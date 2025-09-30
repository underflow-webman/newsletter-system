"""Email template engine implementations."""

from __future__ import annotations

from typing import Dict, Any, Optional
from .interfaces import IEmailTemplateEngine


class Jinja2TemplateEngine(IEmailTemplateEngine):
    """Jinja2 template engine for email templates."""
    
    def __init__(self, template_dir: str = "templates", config: Optional[Dict[str, Any]] = None):
        self.template_dir = template_dir
        self.config = config or {}
        self._env = None
    
    async def _setup_environment(self) -> None:
        """Setup Jinja2 environment."""
        from jinja2 import Environment, FileSystemLoader
        
        if not self._env:
            self._env = Environment(
                loader=FileSystemLoader(self.template_dir),
                **self.config
            )
    
    async def render_template(self, template_name: str, context: Dict[str, Any]) -> str:
        """Render email template with context."""
        if not self._env:
            await self._setup_environment()
        
        template = self._env.get_template(template_name)
        return template.render(**context)
    
    async def render_string(self, template_string: str, context: Dict[str, Any]) -> str:
        """Render template string with context."""
        if not self._env:
            await self._setup_environment()
        
        template = self._env.from_string(template_string)
        return template.render(**context)
    
    async def validate_template(self, template_name: str) -> bool:
        """Validate template syntax."""
        try:
            if not self._env:
                await self._setup_environment()
            
            self._env.get_template(template_name)
            return True
        except Exception:
            return False


class MakoTemplateEngine(IEmailTemplateEngine):
    """Mako template engine for email templates."""
    
    def __init__(self, template_dir: str = "templates", config: Optional[Dict[str, Any]] = None):
        self.template_dir = template_dir
        self.config = config or {}
        self._lookup = None
    
    async def _setup_lookup(self) -> None:
        """Setup Mako template lookup."""
        from mako.lookup import TemplateLookup
        
        if not self._lookup:
            self._lookup = TemplateLookup(
                directories=[self.template_dir],
                **self.config
            )
    
    async def render_template(self, template_name: str, context: Dict[str, Any]) -> str:
        """Render email template with context."""
        if not self._lookup:
            await self._setup_lookup()
        
        template = self._lookup.get_template(template_name)
        return template.render(**context)
    
    async def render_string(self, template_string: str, context: Dict[str, Any]) -> str:
        """Render template string with context."""
        if not self._lookup:
            await self._setup_lookup()
        
        from mako.template import Template
        template = Template(template_string, lookup=self._lookup)
        return template.render(**context)
    
    async def validate_template(self, template_name: str) -> bool:
        """Validate template syntax."""
        try:
            if not self._lookup:
                await self._setup_lookup()
            
            self._lookup.get_template(template_name)
            return True
        except Exception:
            return False

