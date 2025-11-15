#!/usr/bin/env python3
"""
Enhanced GitHub Scraper with OpenRouter AI Analysis
Scrapes all repositories with README files and generates AI-powered project summaries.
"""
import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from github import Github, GithubException
from dotenv import load_dotenv
from openai import OpenAI
import time


class EnhancedGitHubScraper:
    """Scrapes GitHub repositories and generates AI-powered project summaries."""
    
    def __init__(self, github_token: Optional[str] = None, openrouter_api_key: Optional[str] = None):
        """
        Initialize GitHub scraper with OpenRouter AI.
        
        Args:
            github_token: GitHub personal access token
            openrouter_api_key: OpenRouter API key for GPT-5 analysis
        """
        self.github = Github(github_token) if github_token else Github()
        self.github_token = github_token
        
        # Initialize OpenRouter client
        self.openrouter_client = None
        if openrouter_api_key:
            self.openrouter_client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=openrouter_api_key,
            )
        
        print(f"[GitHub Scraper] Initialized with {'authenticated' if github_token else 'unauthenticated'} access")
        print(f"[OpenRouter] AI analysis {'enabled' if self.openrouter_client else 'disabled'}")
        print(f"[System Log] Learning: GitHub scraper ready to analyze repositories")
    
    def get_repository_readme(self, repo) -> Optional[str]:
        """
        Get README content from a repository.
        
        Args:
            repo: PyGithub repository object
            
        Returns:
            README content as string or None if not found
        """
        try:
            readme = repo.get_readme()
            content = readme.decoded_content.decode('utf-8')
            print(f"  ✓ README found ({len(content)} characters)")
            print(f"[System Log] Learning: {repo.full_name} has a README with {len(content)} characters")
            return content
        except GithubException as e:
            if e.status == 404:
                print(f"  ⚠ No README found")
            elif e.status == 403:
                print(f"  ⚠ Rate limit hit while fetching README")
            else:
                print(f"  ✗ Error fetching README: {e}")
            return None
        except Exception as e:
            print(f"  ✗ Error decoding README: {e}")
            return None
    
    def scrape_all_repositories(self, username: str) -> List[Dict]:
        """
        Scrape all repositories for a user with full details including README.
        
        Args:
            username: GitHub username
            
        Returns:
            List of repository data dictionaries
        """
        print(f"\n{'='*80}")
        print(f"SCRAPING ALL REPOSITORIES FOR: {username}")
        print(f"{'='*80}\n")
        
        try:
            user = self.github.get_user(username)
            repositories = []
            
            total_repos = user.public_repos
            print(f"[Scraping] Found {total_repos} public repositories\n")
            
            for idx, repo in enumerate(user.get_repos(), 1):
                try:
                    print(f"[{idx}/{total_repos}] Processing: {repo.full_name}")
                    
                    # Get README
                    readme_content = self.get_repository_readme(repo)
                    
                    # Build repository data
                    repo_data = {
                        'name': repo.name,
                        'full_name': repo.full_name,
                        'description': repo.description,
                        'url': repo.html_url,
                        'language': repo.language,
                        'stars': repo.stargazers_count,
                        'forks': repo.forks_count,
                        'watchers': repo.watchers_count,
                        'open_issues': repo.open_issues_count,
                        'created_at': repo.created_at.isoformat() if repo.created_at else None,
                        'updated_at': repo.updated_at.isoformat() if repo.updated_at else None,
                        'pushed_at': repo.pushed_at.isoformat() if repo.pushed_at else None,
                        'size': repo.size,
                        'is_fork': repo.fork,
                        'is_private': repo.private,
                        'default_branch': repo.default_branch,
                        'license': repo.license.name if repo.license else None,
                        'homepage': repo.homepage,
                        'readme': readme_content,
                    }
                    
                    # Get topics
                    try:
                        repo_data['topics'] = repo.get_topics()
                        print(f"  ✓ Topics: {', '.join(repo_data['topics']) if repo_data['topics'] else 'none'}")
                    except Exception as e:
                        print(f"  ⚠ Could not fetch topics: {e}")
                        repo_data['topics'] = []
                    
                    # Get languages
                    try:
                        languages = repo.get_languages()
                        repo_data['languages'] = languages
                        if languages:
                            total_bytes = sum(languages.values())
                            repo_data['languages_breakdown'] = {
                                lang: {
                                    'bytes': bytes_count,
                                    'percentage': round((bytes_count / total_bytes * 100), 2)
                                }
                                for lang, bytes_count in languages.items()
                            }
                            print(f"  ✓ Languages: {', '.join(languages.keys())}")
                            print(f"[System Log] Learning: {repo.full_name} uses languages: {', '.join(languages.keys())}")
                    except Exception as e:
                        print(f"  ⚠ Could not fetch languages: {e}")
                        repo_data['languages'] = {}
                        repo_data['languages_breakdown'] = {}
                    
                    repositories.append(repo_data)
                    print(f"  ✓ Repository scraped successfully ({repo.stargazers_count} ⭐)\n")
                    
                    # Small delay to avoid rate limits
                    time.sleep(0.5)
                    
                except GithubException as e:
                    if e.status == 403:
                        print(f"\n⚠ Rate limit hit! Collected {len(repositories)} repos so far.")
                        print(f"[System Log] Rate limit reached after processing {len(repositories)} repositories")
                        break
                    else:
                        print(f"  ✗ Error scraping {repo.full_name}: {e}\n")
                        continue
                except Exception as e:
                    print(f"  ✗ Unexpected error: {e}\n")
                    continue
            
            print(f"{'='*80}")
            print(f"SCRAPING COMPLETE: {len(repositories)} repositories collected")
            print(f"{'='*80}\n")
            print(f"[System Log] Successfully scraped {len(repositories)} repositories with README files")
            
            return repositories
            
        except GithubException as e:
            print(f"❌ Error accessing user {username}: {e}")
            raise
    
    def generate_project_summary(self, repo_data: Dict) -> Optional[str]:
        """
        Generate AI-powered project summary using OpenRouter GPT-5.
        
        Args:
            repo_data: Repository data dictionary
            
        Returns:
            AI-generated project summary or None if failed
        """
        if not self.openrouter_client:
            print(f"  ⚠ OpenRouter not configured, skipping AI analysis")
            return None
        
        print(f"  🤖 Generating AI summary for {repo_data['name']}...")
        
        # Prepare context for AI
        context = f"""Repository Name: {repo_data['name']}
Description: {repo_data.get('description') or 'No description provided'}
Language: {repo_data.get('language') or 'Not specified'}
Stars: {repo_data['stars']}
Forks: {repo_data['forks']}
Topics: {', '.join(repo_data.get('topics', [])) or 'None'}
"""
        
        # Add languages breakdown if available
        if repo_data.get('languages_breakdown'):
            context += "\nLanguages Used:\n"
            for lang, details in repo_data['languages_breakdown'].items():
                context += f"  - {lang}: {details['percentage']}%\n"
        
        # Add README if available
        readme = repo_data.get('readme')
        if readme:
            # Limit README to first 5000 characters to avoid token limits
            readme_excerpt = readme[:5000] + ("..." if len(readme) > 5000 else "")
            context += f"\nREADME Content:\n{readme_excerpt}\n"
        
        # Create prompt for GPT-5
        prompt = f"""Analyze this GitHub repository and create a comprehensive project summary:

{context}

Please provide:
1. Project Overview - What the project does and its main purpose
2. Key Features - Main features and capabilities
3. Technology Stack - Technologies, frameworks, and tools used
4. Use Cases - Potential use cases and target audience
5. Technical Highlights - Notable implementation details or architecture
6. Development Status - Current state and activity level

Keep the summary detailed but concise, technical but accessible."""

        try:
            response = self.openrouter_client.chat.completions.create(
                model="openai/gpt-4o",  # Using GPT-4o as it's more cost-effective
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert software engineer and technical writer analyzing GitHub repositories. Provide detailed, insightful project summaries."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=1500,
                temperature=0.7,
            )
            
            summary = response.choices[0].message.content
            print(f"  ✓ AI summary generated ({len(summary)} characters)")
            print(f"[System Log] Learning: Generated AI summary for {repo_data['name']} using GPT-4o")
            
            return summary
            
        except Exception as e:
            print(f"  ✗ Error generating AI summary: {e}")
            print(f"[System Log] Failed to generate AI summary for {repo_data['name']}: {str(e)}")
            return None
    
    def save_project_summaries(self, repositories: List[Dict], username: str, output_dir: str = "project_summaries"):
        """
        Generate and save AI summaries for all repositories.
        
        Args:
            repositories: List of repository data
            username: GitHub username
            output_dir: Directory to save summaries
        """
        print(f"\n{'='*80}")
        print(f"GENERATING PROJECT SUMMARIES")
        print(f"{'='*80}\n")
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        summaries = []
        
        for idx, repo in enumerate(repositories, 1):
            print(f"\n[{idx}/{len(repositories)}] Processing: {repo['name']}")
            
            # Generate AI summary
            ai_summary = self.generate_project_summary(repo)
            
            # Create comprehensive summary
            project_summary = {
                'repository': repo['name'],
                'full_name': repo['full_name'],
                'url': repo['url'],
                'description': repo.get('description'),
                'language': repo.get('language'),
                'stars': repo['stars'],
                'forks': repo['forks'],
                'topics': repo.get('topics', []),
                'ai_summary': ai_summary,
                'has_readme': repo.get('readme') is not None,
                'analyzed_at': datetime.now().isoformat(),
            }
            
            summaries.append(project_summary)
            
            # Save individual project summary to text file
            safe_repo_name = repo['name'].replace('/', '_').replace(' ', '_')
            text_file = os.path.join(output_dir, f"{safe_repo_name}.txt")
            
            with open(text_file, 'w', encoding='utf-8') as f:
                f.write(f"{'='*80}\n")
                f.write(f"PROJECT SUMMARY: {repo['name']}\n")
                f.write(f"{'='*80}\n\n")
                f.write(f"Repository: {repo['full_name']}\n")
                f.write(f"URL: {repo['url']}\n")
                f.write(f"Language: {repo.get('language') or 'Not specified'}\n")
                f.write(f"Stars: {repo['stars']} | Forks: {repo['forks']}\n")
                f.write(f"Topics: {', '.join(repo.get('topics', [])) or 'None'}\n")
                f.write(f"\nDescription:\n{repo.get('description') or 'No description provided'}\n")
                
                if ai_summary:
                    f.write(f"\n{'─'*80}\n")
                    f.write(f"AI-POWERED ANALYSIS\n")
                    f.write(f"{'─'*80}\n\n")
                    f.write(ai_summary)
                    f.write(f"\n\n")
                
                if repo.get('readme'):
                    f.write(f"\n{'─'*80}\n")
                    f.write(f"README CONTENT\n")
                    f.write(f"{'─'*80}\n\n")
                    f.write(repo['readme'])
                
                f.write(f"\n\n{'='*80}\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"{'='*80}\n")
            
            print(f"  ✓ Saved to: {text_file}")
            print(f"[System Log] Saved project summary for {repo['name']} to {text_file}")
            
            # Small delay between API calls
            time.sleep(1)
        
        # Save consolidated JSON summary
        summary_json = os.path.join(output_dir, f"{username}_all_projects_summary.json")
        with open(summary_json, 'w', encoding='utf-8') as f:
            json.dump(summaries, f, indent=2, ensure_ascii=False)
        
        print(f"\n{'='*80}")
        print(f"ALL SUMMARIES SAVED")
        print(f"{'='*80}")
        print(f"📁 Output directory: {output_dir}")
        print(f"📄 Individual summaries: {len(summaries)} text files")
        print(f"📊 Consolidated JSON: {summary_json}")
        print(f"{'='*80}\n")
        print(f"[System Log] Generated and saved {len(summaries)} project summaries")
        
        return summaries
    
    def scrape_and_analyze(self, username: str, output_dir: str = "project_summaries") -> Dict:
        """
        Complete workflow: scrape repositories and generate AI summaries.
        
        Args:
            username: GitHub username
            output_dir: Directory to save summaries
            
        Returns:
            Complete analysis data
        """
        start_time = datetime.now()
        
        # Step 1: Scrape all repositories
        repositories = self.scrape_all_repositories(username)
        
        if not repositories:
            print("❌ No repositories found or error occurred")
            return {'error': 'No repositories found'}
        
        # Step 2: Generate and save project summaries
        summaries = self.save_project_summaries(repositories, username, output_dir)
        
        # Calculate statistics
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        stats = {
            'username': username,
            'total_repositories': len(repositories),
            'repositories_with_readme': sum(1 for r in repositories if r.get('readme')),
            'repositories_with_ai_summary': sum(1 for s in summaries if s.get('ai_summary')),
            'total_stars': sum(r['stars'] for r in repositories),
            'total_forks': sum(r['forks'] for r in repositories),
            'languages_used': list(set(r['language'] for r in repositories if r.get('language'))),
            'processing_time_seconds': duration,
            'analyzed_at': datetime.now().isoformat(),
        }
        
        # Save stats
        stats_file = os.path.join(output_dir, f"{username}_statistics.json")
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
        
        print(f"\n{'='*80}")
        print(f"ANALYSIS COMPLETE")
        print(f"{'='*80}")
        print(f"👤 User: {username}")
        print(f"📦 Repositories: {stats['total_repositories']}")
        print(f"📄 With README: {stats['repositories_with_readme']}")
        print(f"🤖 AI Summaries: {stats['repositories_with_ai_summary']}")
        print(f"⭐ Total Stars: {stats['total_stars']}")
        print(f"🔱 Total Forks: {stats['total_forks']}")
        print(f"💻 Languages: {', '.join(stats['languages_used'][:10])}")
        print(f"⏱️  Time: {duration:.1f} seconds")
        print(f"{'='*80}\n")
        print(f"[System Log] Complete analysis finished. Processed {stats['total_repositories']} repos in {duration:.1f}s")
        
        return {
            'repositories': repositories,
            'summaries': summaries,
            'statistics': stats,
        }


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Enhanced GitHub Scraper with AI-Powered Project Analysis',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scrape all repos and generate AI summaries
  python github_scraper_enhanced.py baladhurgesh
  
  # Custom output directory
  python github_scraper_enhanced.py baladhurgesh -o my_summaries
  
  # Provide API keys via command line
  python github_scraper_enhanced.py baladhurgesh --github-token YOUR_TOKEN --openrouter-key YOUR_KEY

Note: This script uses OpenRouter API with GPT-4o for analysis.
Make sure to set OPENROUTER_API_KEY in your .env file or provide it via --openrouter-key.
        """
    )
    
    parser.add_argument('username', help='GitHub username to analyze')
    parser.add_argument('-o', '--output', default='project_summaries',
                       help='Output directory for summaries (default: project_summaries)')
    parser.add_argument('--github-token', help='GitHub token (overrides .env)')
    parser.add_argument('--openrouter-key', help='OpenRouter API key (overrides .env)')
    
    args = parser.parse_args()
    
    # Load environment variables
    load_dotenv()
    
    # Get API keys
    github_token = args.github_token or os.getenv('GITHUB_TOKEN')
    openrouter_key = args.openrouter_key or os.getenv('OPENROUTER_API_KEY')
    
    if not github_token:
        print("\n⚠️  WARNING: No GitHub token provided!")
        print("   You may hit rate limits. Get a token at:")
        print("   https://github.com/settings/tokens\n")
    
    if not openrouter_key:
        print("\n⚠️  WARNING: No OpenRouter API key provided!")
        print("   AI summaries will be skipped. Get a key at:")
        print("   https://openrouter.ai/keys\n")
    
    # Create scraper
    scraper = EnhancedGitHubScraper(
        github_token=github_token,
        openrouter_api_key=openrouter_key
    )
    
    # Run analysis
    try:
        scraper.scrape_and_analyze(
            username=args.username,
            output_dir=args.output
        )
        print("\n✅ Analysis completed successfully!")
        print(f"[System Log] All project information saved to {args.output}/")
        return 0
    except Exception as e:
        print(f"\n❌ Analysis failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    exit(main())

