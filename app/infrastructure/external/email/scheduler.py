"""Email scheduling implementations."""

from __future__ import annotations

import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from .interfaces import IEmailScheduler


class AsyncEmailScheduler(IEmailScheduler):
    """Asynchronous email scheduler."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self._scheduled_emails: Dict[str, Dict[str, Any]] = {}
        self._running = False
        self._task = None
    
    async def schedule_email(self, email_data: Dict[str, Any], send_at: datetime) -> str:
        """Schedule email for future sending."""
        schedule_id = f"schedule_{datetime.utcnow().timestamp()}"
        
        scheduled_email = {
            "id": schedule_id,
            "email_data": email_data,
            "send_at": send_at,
            "created_at": datetime.utcnow(),
            "status": "scheduled"
        }
        
        self._scheduled_emails[schedule_id] = scheduled_email
        
        # Start processing if not already running
        if not self._running:
            await self.start_processing()
        
        return schedule_id
    
    async def cancel_scheduled_email(self, schedule_id: str) -> bool:
        """Cancel scheduled email."""
        if schedule_id in self._scheduled_emails:
            self._scheduled_emails[schedule_id]["status"] = "cancelled"
            return True
        return False
    
    async def get_scheduled_emails(self, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """Get scheduled emails in date range."""
        emails = list(self._scheduled_emails.values())
        
        if start_date:
            emails = [e for e in emails if e["send_at"] >= start_date]
        
        if end_date:
            emails = [e for e in emails if e["send_at"] <= end_date]
        
        return emails
    
    async def process_scheduled_emails(self) -> int:
        """Process and send scheduled emails."""
        now = datetime.utcnow()
        processed_count = 0
        
        for schedule_id, email_info in self._scheduled_emails.items():
            if email_info["status"] == "scheduled" and email_info["send_at"] <= now:
                try:
                    # Here you would call the actual email service
                    # await self._email_service.send_bulk_email(...)
                    email_info["status"] = "sent"
                    email_info["sent_at"] = now
                    processed_count += 1
                except Exception as e:
                    email_info["status"] = "failed"
                    email_info["error"] = str(e)
        
        return processed_count
    
    async def start_processing(self) -> None:
        """Start the email processing loop."""
        if self._running:
            return
        
        self._running = True
        self._task = asyncio.create_task(self._processing_loop())
    
    async def stop_processing(self) -> None:
        """Stop the email processing loop."""
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
    
    async def _processing_loop(self) -> None:
        """Main processing loop for scheduled emails."""
        while self._running:
            try:
                await self.process_scheduled_emails()
                await asyncio.sleep(60)  # Check every minute
            except asyncio.CancelledError:
                break
            except Exception as e:
                # Log error and continue
                print(f"Error in email processing loop: {e}")
                await asyncio.sleep(60)

