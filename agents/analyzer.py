import os
import json
import aiohttp
import asyncio
from config.manager import ConfigManager
from pathlib import Path
from colorama import Fore, Style

class OpenRouterAnalyzer:
    def __init__(self, db):
        self.config = ConfigManager()
        self.db = db
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.config.openrouter_api_key}",
            "Content-Type": "application/json"
        }
        self.analysis_folder = Path("analysis")
        self.analysis_folder.mkdir(exist_ok=True)

    async def analyze_urls(self, urls):
        try:
            print(f"{Fore.CYAN}Analyzing {len(urls)} URLs...{Style.RESET_ALL}")
            
            with self.db.conn:
                cursor = self.db.conn.cursor()
                content_list = []
                for url in urls:
                    cursor.execute('''SELECT content FROM seo_content 
                                   JOIN urls ON seo_content.url_id = urls.id 
                                   WHERE urls.url = ?''', (url,))
                    result = cursor.fetchone()
                    if result:
                        content_list.append(f"URL: {url}\nContent:\n{result[0]}")
            
            combined_content = "\n\n".join(content_list)
            
            prompt = f"""
            Based on this specific content from our database, create a focused SEO report:
            {combined_content}
            
            Include these sections:
            1. Metadata Recommendations:
               - Title tag (60 chars max)
               - Meta description (160 chars max)
               - URL structure (just the path, not the domain)
               - Follow SEO best practices
            
            2. Content Outline:
               - Suggested heading structure
               - Key sections to include
               - Logical flow
            
            3. Keyword Analysis:
               - Primary keywords (5-10)
               - Secondary keywords (10-15)
               - Long-tail opportunities
            
            4. Actionable Recommendations:
               - Content improvements
               - SEO optimizations
               - Engagement strategies

            5. Table:
               Include tips for how the keywords can be used in the content.

            Provide a detailed report with actionable recommendations.
            
            Keep it specific to this content. No generic advice.
            """
            
            payload = {
                "model": self.config.ai_model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
                "max_tokens": 2000
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(self.base_url, headers=self.headers, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data['choices'][0]['message']['content']
                    else:
                        error = await response.text()
                        raise Exception(f"OpenRouter API error: {error}")
                        
        except Exception as e:
            print(f"{Fore.RED}Error during analysis: {e}{Style.RESET_ALL}")
            return None

    def _get_content_for_url(self, url):
        # Implement content retrieval from your database or storage
        pass

    async def save_report(self, report):
        report_path = self.analysis_folder / "aggregated_analysis.txt"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"{Fore.GREEN}Aggregated report saved to {report_path}{Style.RESET_ALL}")

async def main(urls):
    analyzer = OpenRouterAnalyzer()
    report = await analyzer.analyze_urls(urls)
    if report:
        await analyzer.save_report(report)

# Example usage
if __name__ == "__main__":
    urls = [
        "https://example.com/page1",
        "https://example.com/page2",
        "https://example.com/page3",
        "https://example.com/page4",
        "https://example.com/page5"
    ]
    asyncio.run(main(urls)) 