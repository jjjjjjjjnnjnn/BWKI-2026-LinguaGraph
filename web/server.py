"""
LinguaGraph Web Server

Simple HTTP server that serves the frontend and provides API endpoints
for the analysis pipeline.

Usage:
    python web/server.py
    # Open http://localhost:8080
"""

import json
import sys
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from extract import extract_concepts
from graph import build_graph, load_expert_graph, graph_to_dict
from compare import detect_missing_links
from scoring import calculate_lds_score
from explain import generate_simple_explanation
from providers import get_provider


class LinguaGraphHandler(SimpleHTTPRequestHandler):
    """Handle HTTP requests for LinguaGraph web app."""

    def do_GET(self):
        if self.path == '/':
            self.path = '/web/index.html'
        elif self.path == '/demo':
            self.path = '/web/demo.html'
        elif self.path.startswith('/api/'):
            self.handle_api()
            return
        return super().do_GET()

    def do_POST(self):
        if self.path == '/api/analyze':
            self.handle_analyze()
            return
        self.send_error(404)

    def handle_api(self):
        """Handle API GET requests."""
        if self.path == '/api/health':
            # Check LLM availability
            try:
                provider = get_provider()
                self.send_json({
                    "status": "ok",
                    "version": "0.2.0",
                    "llm_provider": repr(provider)
                })
            except Exception as e:
                self.send_json({
                    "status": "degraded",
                    "error": str(e)
                }, 503)
        else:
            self.send_error(404)

    def handle_analyze(self):
        """Handle analysis request."""
        try:
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            data = json.loads(body.decode('utf-8'))

            answer = data.get('answer', '')
            language = data.get('language', 'zh')
            topic = data.get('topic', 'derivative')

            if not answer.strip():
                self.send_json({"error": "Empty answer"}, 400)
                return

            # Step 1: Extract concepts (uses real LLM from config)
            extracted = extract_concepts(answer, language)

            # Step 2: Build student graph
            student_graph = build_graph(extracted)

            # Step 3: Load expert graph
            try:
                expert_graph = load_expert_graph("calculus")
            except FileNotFoundError:
                expert_graph = load_expert_graph("social_issues")

            # Step 4: Detect missing links
            missing = detect_missing_links(student_graph, expert_graph)

            # Step 5: Calculate LDS (full 3-component formula: GED + node Jaccard + edge Jaccard)
            lds_result = calculate_lds_score(student_graph, expert_graph)
            lds = lds_result["lds_score"]

            # Step 6: Generate explanation
            explanation = generate_simple_explanation(missing, language)

            # Build response
            student_data = graph_to_dict(student_graph)
            expert_data = graph_to_dict(expert_graph)

            result = {
                "student_graph": student_data,
                "expert_graph": expert_data,
                "missing_links": missing,
                "lds": lds,
                "explanation": explanation,
                "stats": {
                    "concepts_extracted": len(extracted.get("concepts", [])),
                    "relations_extracted": len(extracted.get("relations", [])),
                    "missing_links_count": len(missing),
                }
            }

            self.send_json(result)

        except Exception as e:
            self.send_json({"error": str(e)}, 500)

    def send_json(self, data, status=200):
        """Send JSON response."""
        response = json.dumps(data, ensure_ascii=False, indent=2)
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', 'http://localhost:8080')
        self.end_headers()
        self.wfile.write(response.encode('utf-8'))


def main():
    port = 8080
    server = HTTPServer(('localhost', port), LinguaGraphHandler)
    print(f"LinguaGraph server running at http://localhost:{port}")
    print("Press Ctrl+C to stop")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")


if __name__ == '__main__':
    main()
