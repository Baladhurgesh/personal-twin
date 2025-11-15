#!/usr/bin/env python3
"""
ElevenLabs Knowledge Base Integration
Handles uploading project summaries and resumes to ElevenLabs knowledge base.
"""
import os
from typing import Optional, List, Dict
from elevenlabs.client import ElevenLabs


class ElevenLabsKnowledgeBase:
    """Manages ElevenLabs knowledge base operations."""
    
    def __init__(self, api_key: Optional[str] = None, agent_id: Optional[str] = None):
        """
        Initialize ElevenLabs knowledge base client.
        
        Args:
            api_key: ElevenLabs API key
            agent_id: ElevenLabs agent ID (optional, for updating agent)
        """
        self.api_key = api_key
        self.agent_id = agent_id
        self.client = None
        
        if api_key:
            self.client = ElevenLabs(api_key=api_key)
            print(f"[ElevenLabs KB] Initialized with API key")
        else:
            print(f"[ElevenLabs KB] Warning: No API key provided")
    
    def create_document_from_text(self, text: str, name: str) -> Optional[Dict]:
        """
        Create a knowledge base document from text.
        
        Args:
            text: Text content to upload
            name: Name for the document
            
        Returns:
            Document info dict or None if failed
        """
        if not self.client:
            print(f"[ElevenLabs KB] Error: Client not initialized")
            return None
        
        try:
            print(f"[ElevenLabs KB] Creating text document: {name}")
            
            document = self.client.conversational_ai.knowledge_base.documents.create_from_text(
                text=text,
                name=name
            )
            
            print(f"[ElevenLabs KB] ✓ Text document created: {name} (ID: {document.id})")
            print(f"[System Log] Added to knowledge base: {name}")
            
            return {
                'type': 'text',
                'name': document.name,
                'id': document.id,
                'status': 'success'
            }
            
        except Exception as e:
            print(f"[ElevenLabs KB] Error creating text document: {e}")
            return None
    
    def create_document_from_file(self, file_path: str, name: str) -> Optional[Dict]:
        """
        Create a knowledge base document from a file.
        
        Args:
            file_path: Path to the file
            name: Name for the document
            
        Returns:
            Document info dict or None if failed
        """
        if not self.client:
            print(f"[ElevenLabs KB] Error: Client not initialized")
            return None
        
        if not os.path.exists(file_path):
            print(f"[ElevenLabs KB] Error: File not found: {file_path}")
            return None
        
        try:
            print(f"[ElevenLabs KB] Creating file document: {name}")
            
            with open(file_path, 'rb') as f:
                document = self.client.conversational_ai.knowledge_base.documents.create_from_file(
                    file=f,
                    name=name
                )
            
            print(f"[ElevenLabs KB] ✓ File document created: {name} (ID: {document.id})")
            print(f"[System Log] Added to knowledge base: {name} from {file_path}")
            
            return {
                'type': 'file',
                'name': document.name,
                'id': document.id,
                'status': 'success'
            }
            
        except Exception as e:
            print(f"[ElevenLabs KB] Error creating file document: {e}")
            return None
    
    def upload_project_summary(self, summary_file_path: str, project_name: str) -> Optional[Dict]:
        """
        Upload a project summary text file to knowledge base.
        
        Args:
            summary_file_path: Path to the summary text file
            project_name: Name of the project
            
        Returns:
            Document info dict or None if failed
        """
        if not os.path.exists(summary_file_path):
            print(f"[ElevenLabs KB] Error: Summary file not found: {summary_file_path}")
            return None
        
        try:
            # Read the summary file
            with open(summary_file_path, 'r', encoding='utf-8') as f:
                text_content = f.read()
            
            # Create document with descriptive name
            doc_name = f"GitHub Project: {project_name}"
            return self.create_document_from_text(text_content, doc_name)
            
        except Exception as e:
            print(f"[ElevenLabs KB] Error uploading project summary: {e}")
            return None
    
    def upload_all_project_summaries(self, summaries_dir: str, username: str) -> List[Dict]:
        """
        Upload all project summaries from a directory to knowledge base.
        
        Args:
            summaries_dir: Directory containing summary .txt files
            username: GitHub username
            
        Returns:
            List of uploaded document info dicts
        """
        if not os.path.exists(summaries_dir):
            print(f"[ElevenLabs KB] Error: Directory not found: {summaries_dir}")
            return []
        
        uploaded_docs = []
        
        # Get all .txt files in the directory (excluding statistics and summary JSONs)
        txt_files = [f for f in os.listdir(summaries_dir) 
                     if f.endswith('.txt') and not f.startswith('_')]
        
        print(f"\n[ElevenLabs KB] Uploading {len(txt_files)} project summaries for {username}...")
        
        for txt_file in txt_files:
            # Extract project name from filename
            project_name = txt_file.replace('.txt', '').replace('_', ' ')
            file_path = os.path.join(summaries_dir, txt_file)
            
            # Upload the summary
            doc_info = self.upload_project_summary(file_path, project_name)
            
            if doc_info:
                uploaded_docs.append(doc_info)
        
        print(f"[ElevenLabs KB] ✓ Successfully uploaded {len(uploaded_docs)} project summaries")
        print(f"[System Log] Uploaded {len(uploaded_docs)} GitHub project summaries to knowledge base")
        
        return uploaded_docs
    
    def upload_resume(self, resume_file_path: str, username: str) -> Optional[Dict]:
        """
        Upload a resume PDF to knowledge base.
        
        Args:
            resume_file_path: Path to the resume PDF file
            username: User's name or identifier
            
        Returns:
            Document info dict or None if failed
        """
        doc_name = f"Resume: {username}"
        return self.create_document_from_file(resume_file_path, doc_name)
    
    def update_agent_knowledge_base(self, document_ids: List[Dict]) -> bool:
        """
        Update the agent's knowledge base with uploaded documents.
        
        Args:
            document_ids: List of document info dicts with 'type', 'name', 'id'
            
        Returns:
            True if successful, False otherwise
        """
        if not self.client or not self.agent_id:
            print(f"[ElevenLabs KB] Warning: Agent ID not configured, skipping agent update")
            return False
        
        try:
            print(f"[ElevenLabs KB] Updating agent {self.agent_id} with {len(document_ids)} documents...")
            
            # Format documents for agent update
            knowledge_base_items = [
                {
                    "type": doc['type'],
                    "name": doc['name'],
                    "id": doc['id']
                }
                for doc in document_ids
            ]
            
            # Update agent configuration
            agent = self.client.conversational_ai.agents.update(
                agent_id=self.agent_id,
                conversation_config={
                    "agent": {
                        "prompt": {
                            "knowledge_base": knowledge_base_items
                        }
                    }
                }
            )
            
            print(f"[ElevenLabs KB] ✓ Agent updated successfully")
            print(f"[System Log] Updated ElevenLabs agent with {len(document_ids)} documents")
            
            return True
            
        except Exception as e:
            print(f"[ElevenLabs KB] Error updating agent: {e}")
            return False
    
    def get_all_documents(self) -> List[Dict]:
        """
        Get all documents in the knowledge base.
        
        Returns:
            List of document info dicts
        """
        if not self.client:
            print(f"[ElevenLabs KB] Error: Client not initialized")
            return []
        
        try:
            # Note: This is a placeholder - actual API might differ
            print(f"[ElevenLabs KB] Retrieving all documents...")
            documents = self.client.conversational_ai.knowledge_base.documents.get_all()
            print(f"[ElevenLabs KB] Found {len(documents)} documents")
            return documents
            
        except Exception as e:
            print(f"[ElevenLabs KB] Error retrieving documents: {e}")
            return []


def main():
    """Test the knowledge base integration."""
    from dotenv import load_dotenv
    import argparse
    
    load_dotenv()
    
    parser = argparse.ArgumentParser(description='ElevenLabs Knowledge Base Manager')
    parser.add_argument('--test-text', help='Test uploading text')
    parser.add_argument('--test-file', help='Test uploading a file')
    parser.add_argument('--upload-summaries', help='Upload all summaries from directory')
    parser.add_argument('--username', help='Username for context')
    
    args = parser.parse_args()
    
    api_key = os.getenv('ELEVENLABS_API_KEY')
    agent_id = os.getenv('ELEVENLABS_AGENT_ID')
    
    if not api_key:
        print("Error: ELEVENLABS_API_KEY not found in environment")
        return 1
    
    kb = ElevenLabsKnowledgeBase(api_key=api_key, agent_id=agent_id)
    
    if args.test_text:
        result = kb.create_document_from_text(args.test_text, "Test Document")
        print(f"Result: {result}")
    
    elif args.test_file:
        result = kb.create_document_from_file(args.test_file, "Test File Upload")
        print(f"Result: {result}")
    
    elif args.upload_summaries and args.username:
        results = kb.upload_all_project_summaries(args.upload_summaries, args.username)
        print(f"Uploaded {len(results)} summaries")
    
    else:
        print("Please provide a test option. Use --help for details.")
    
    return 0


if __name__ == '__main__':
    exit(main())

