from app.clients.edinet import fetch_document_list
from datetime import date

class ApiTestService:

    def get_testApiRes(
        self,
        target_date: date
    ) -> str:
        res = fetch_document_list(target_date)
        return res
