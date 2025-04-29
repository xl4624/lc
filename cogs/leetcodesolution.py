import discord
from discord.ext import commands
from discord import app_commands, ui
import re, io
import urllib.parse
import validators

class CodeModal(ui.Modal, title="Paste your solution"):
    language     = ui.TextInput(label="language (python, cpp, java, etc.)", max_length=20)
    code         = ui.TextInput(label="solution code", style=discord.TextStyle.paragraph)
    question_url = ui.TextInput(label="leetcode link", placeholder="https://leetcode.com/problems/two-sum")

    def __init__(self, parent_cog: "LeetcodeSolution"):
        super().__init__()
        self.parent_cog = parent_cog

    async def on_submit(self, interaction: discord.Interaction):
        if not self.parent_cog.is_valid_leetcode_link(self.question_url.value):
            await interaction.response.send_message(
                "⚠️ Invalid LeetCode URL. Please provide a valid LeetCode problem link.",
                ephemeral=True
            )
            return
            
        normalized_language = self.parent_cog.normalize_language(self.language.value)
        if normalized_language not in self.parent_cog.language_map.values():
            await interaction.response.send_message(
                f"⚠️ Unsupported language: '{self.language.value}'. Please use one of the supported languages.",
                ephemeral=True
            )
            return
        
        await self.parent_cog.handle_solution(
            interaction,
            normalized_language,
            self.code.value,
            self.question_url.value,
        )

class LeetcodeSolution(commands.Cog):
    def __init__(self, bot): 
        self.bot = bot
        
        self.language_map = {
            # Python variants
            "python": "python", "py": "python", "python3": "python", 
            "python2": "python", "py3": "python", "py2": "python",
            
            # JavaScript variants
            "javascript": "javascript", "js": "javascript", "node": "javascript",
            "nodejs": "javascript",
            
            # TypeScript
            "typescript": "typescript", "ts": "typescript",
            
            # Java
            "java": "java",
            
            # C/C++ variants
            "c": "c", "c++": "cpp", "cpp": "cpp", "cplusplus": "cpp",
            
            # C#
            "c#": "csharp", "csharp": "csharp", "cs": "csharp",
            
            # Other languages
            "go": "go", "golang": "go",
            "ruby": "ruby", "rb": "ruby",
            "rust": "rust", "rs": "rust",
            "php": "php",
            "swift": "swift",
            "kotlin": "kotlin", "kt": "kotlin",
            "scala": "scala",
            "dart": "dart",
            "r": "r",
            "sql": "sql",
            "bash": "bash", "shell": "bash",
        }
        
        # Languages that use || for logical OR
        self.languages_with_or_operator = {
            "java", "c", "cpp", "csharp", "javascript", "typescript", 
            "php", "swift", "kotlin", "dart", "rust", "go"
        }
        
        self.valid_domains = [
            "leetcode.com",
            "leetcode.cn",
            "leetcode-cn.com"
        ]

    @commands.Cog.listener()
    async def on_ready(self): 
        print("Leetcode Solution cog loaded")

    @app_commands.command(name="leetcode", description="Format your LeetCode Solution")
    async def open_modal(self, interaction: discord.Interaction):
        await interaction.response.send_modal(CodeModal(self))

    async def handle_solution(self, interaction, language, code, url):
        await interaction.response.defer(thinking=True) 

        url = self.sanitize_url(url)
        code = self.sanitize_code(code, language)

        title = self._extract_title(url) or "LeetCode Question"
        display_title = f"[{title}]({url})"

        snippet = f"```{language}\n{code}\n```"
        message = f"{display_title}\n\n||{snippet}||"

        if len(message) <= 2_000:
            await interaction.followup.send(message)
        else:
            ext = self._ext(language)
            filename = f"{self.sanitize_filename(title)}.{ext}"
            file = discord.File(io.StringIO(code), filename=filename)
            await interaction.followup.send(f"{display_title}\n\nSolution attached:", file=file)

    def _extract_title(self, link):
        for pat in (r"leetcode\.(?:com|cn)/problems/([^/]+)", r"leetcode(?:-cn)?\.(?:com|cn)/contest/[^/]+/problems/([^/]+)"):
            if (m := re.search(pat, link)):
                slug = m.group(1)
                if (n := re.match(r"^(\d+)-(.+)$", slug)):
                    return f"{n.group(1)}. {n.group(2).replace('-', ' ').title()}"
                return slug.replace('-', ' ').title()
        return None

    def _ext(self, lang):
        return {
            "python": "py", "javascript": "js", "typescript": "ts", "java": "java",
            "cpp": "cpp", "c": "c", "csharp": "cs", "go": "go", "ruby": "rb",
            "rust": "rs", "php": "php", "swift": "swift", "kotlin": "kt",
            "scala": "scala", "dart": "dart", "r": "r", "sql": "sql", "bash": "sh"
        }.get(lang, "txt")
    
    def is_valid_leetcode_link(self, url):
        try:
            if not validators.url(url):
                return False
                
            parsed_url = urllib.parse.urlparse(url)
            
            domain = parsed_url.netloc.lower()
            if not any(domain.endswith(valid_domain) for valid_domain in self.valid_domains):
                return False
                
            path = parsed_url.path.lower()
            return any([
                '/problems/' in path,  
                '/contest/' in path and '/problems/' in path,  
            ])
            
        except Exception:
            return False
    
    def normalize_language(self, language):
        language = language.lower().strip()
        return self.language_map.get(language, language)
    
    def sanitize_url(self, url):
        url = url.strip().strip('"\'')
        
        if validators.url(url):
            parsed = urllib.parse.urlparse(url)
            return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        return url
    
    def sanitize_code(self, code, language):
        # Replace triple backticks to prevent breaking code blocks
        code = code.replace("```", "'''")
        
        # For languages that use || as the OR operator, replace with Unicode vertical line
        # to prevent Discord from interpreting it as a spoiler tag
        if language in self.languages_with_or_operator:
            # Replace || with ⏐⏐ (Unicode Character "⏐" (U+23D0))
            code = re.sub(r'(?<!\\)\|\|', '⏐⏐', code)
        
        return code
    
    def sanitize_filename(self, filename):
        filename = filename.replace(' ', '_')
        filename = re.sub(r'[\\/*?:"<>|]', '', filename)
        if len(filename) > 50:
            filename = filename[:47] + '...'
        return filename
            
async def setup(bot): await bot.add_cog(LeetcodeSolution(bot))
