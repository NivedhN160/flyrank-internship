import pytest
from polite_checker import PoliteChecker
from models import QuoteItem, ScrapeResult
from parser import QuoteParser

def test_polite_checker_robot_rules():
    checker = PoliteChecker(user_agent="FlyRankResearchBot/1.0", default_delay=0.1)
    assert checker.default_delay == 0.1
    # Check rate limit enforcement runs without error
    checker.enforce_rate_limit(0.01)

def test_html_parser_and_pydantic_model():
    sample_html = """
    <html>
        <body>
            <div class="quote">
                <span class="text">“The world as we have created it is a process of our thinking.”</span>
                <span>by <small class="author">Albert Einstein</small>
                <a href="/author/Albert-Einstein">(about)</a>
                </span>
                <div class="tags">
                    <a class="tag" href="/tag/change/page/1/">change</a>
                    <a class="tag" href="/tag/deep-thoughts/page/1/">deep-thoughts</a>
                </div>
            </div>
        </body>
    </html>
    """
    parser = QuoteParser("http://quotes.toscrape.com")
    items, next_page = parser.parse_page(sample_html)
    assert len(items) == 1
    assert items[0].author == "Albert Einstein"
    assert "change" in items[0].tags

    res = ScrapeResult(
        target_domain="quotes.toscrape.com",
        total_scraped=len(items),
        pages_visited=1,
        scraped_at="2026-08-20T22:00:00Z",
        items=items
    )
    assert res.total_scraped == 1
