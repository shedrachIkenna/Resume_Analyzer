import re
from typing import Optional

def extract_email(text: str):
    match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    return match.group(0) if match else None

def extract_phone(text: str):
    match = re.search(r'(\+?\d{1,3})?[\s.-]?(\(?\d{3}\)?[\s.-]?)?\d{3}[\s.-]?\d{4}', text)
    return match.group(0) if match else None

def extract_name(text: str) -> Optional[str]:
    """
    Extract a person's name from text using multiple strategies.
    
    Args:
        text: The input text to search for a name
        
    Returns:
        The extracted name or None if no name could be found
    """
    # Strategy 1: Look for common name patterns with titles
    name_patterns = [
        r'(?:Mr\.|Mrs\.|Ms\.|Miss|Dr\.|Prof\.) [A-Z][a-z]+ (?:[A-Z][a-z]+ )*[A-Z][a-z]+',
        r'[A-Z][a-z]+ (?:[A-Z][a-z]+ )*[A-Z][a-z]+(?:, Ph\.D\.|, MD|, MBA|, CPA)',
        r'^[A-Z][a-z]+ (?:[A-Z][a-z]+ )*[A-Z][a-z]+$'  # Full lines that look like names
    ]
    
    for pattern in name_patterns:
        matches = re.findall(pattern, text)
        if matches:
            return matches[0].strip()
    
    # Strategy 2: Look for lines that are likely to be names (short, capitalized words)
    lines = text.strip().split('\n')
    for line in lines:
        line = line.strip()
        words = line.split()
        
        # Name candidates should have 2-3 words, all properly capitalized
        if 2 <= len(words) <= 3 and all(word[0].isupper() for word in words if word):
            # Check if words are reasonable name length and don't contain non-alpha chars
            if all(2 <= len(word) <= 15 and word.replace('-', '').replace("'", '').isalpha() for word in words):
                return line
    
    # Strategy 3: Look for lines following name indicators
    name_indicators = ["name:", "full name:", "candidate:", "applicant:"]
    for i, line in enumerate(lines):
        lower_line = line.lower()
        for indicator in name_indicators:
            if indicator in lower_line:
                # Check if the name is on this line after the indicator
                name_part = line.split(indicator.replace(':', ''), 1)[-1].strip().strip(':')
                if name_part:
                    return name_part
                # Otherwise check the next line if it exists
                elif i + 1 < len(lines) and lines[i + 1].strip():
                    next_line = lines[i + 1].strip()
                    # Check if next line looks like a name (not too long, capitalized)
                    if len(next_line.split()) <= 4 and not any(char.isdigit() for char in next_line):
                        return next_line
    
    return "Can't find name"

def extract_education(text: str):
    education_keywords = ['bachelor', 'b.sc', 'bsc', 'master', 'msc', 'phd', 'degree', 'university', 'college']
    education_lines = []
    for line in text.split('\n'):
        for keyword in education_keywords:
            if keyword in line.lower():
                education_lines.append(line.strip())
                break
    return education_lines
