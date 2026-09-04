from app.clients.edinet import fetch_document_list
from datetime import date

import json

class ApiTestService:

    def get_testApiRes(
        self,
        target_date: date
    ) -> str:
        response = fetch_document_list(target_date)
        res = json.dumps(response["results"], ensure_ascii=False)
        return res