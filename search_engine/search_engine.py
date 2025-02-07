from whoosh.index import open_dir
from whoosh.qparser import MultifieldParser
from .config import INDEX_DIR, DEFAULT_SEARCH_FIELDS  # 설정값 가져오기
from .utils import setup_logging, validate_query, format_results, print_results  # 유틸리티 함수 가져오기

# 검색 기능 구현
def search(query_str):
    # 로그 설정
    logger = setup_logging()

    # 검색어 유효성 검사
    query_str = validate_query(query_str)

    # 인덱스 열기
    index = open_dir(INDEX_DIR)
    
    # 여러 필드를 동시에 검색할 수 있도록 MultiFieldParser 설정
    parser = MultifieldParser(DEFAULT_SEARCH_FIELDS, index.schema)

    with index.searcher() as searcher:
        query = parser.parse(query_str)
        results = searcher.search(query, limit=None)
        
        # Convert results to a list and sort by predicted_review_star
        sorted_results = sorted(list(results), key=lambda x: x.get('predicted_review_star', 0), reverse=True)
        
        # 검색 결과를 포맷팅하여 출력
        formatted_results = format_results(sorted_results)
        logger.info(f"Search completed for query: {query_str}")
        
        # 결과 반환
        return formatted_results

# 예시 검색
if __name__ == "__main__":
    query = input("Enter your search query: ")
    search(query)
