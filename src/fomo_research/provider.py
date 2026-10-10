import json
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen


API_ROOT = "https://api.fomoapi.io"


class FomoApiError(RuntimeError):
    def __init__(self, status, route):
        self.status = status
        self.route = route
        super().__init__("Fomo API request failed: HTTP {} for {}".format(status, route))


class ApiResponse:
    def __init__(self, route, payload, status, credits_cost, credits_remaining):
        self.route = route
        self.payload = payload
        self.status = status
        self.credits_cost = credits_cost
        self.credits_remaining = credits_remaining


def get_json(route, api_key, params=None, timeout=30):
    query = "?" + urlencode(params) if params else ""
    request_route = route + query
    request = Request(
        API_ROOT + request_route,
        headers={"Authorization": "Bearer " + api_key, "Accept": "application/json"},
        method="GET",
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
            return ApiResponse(
                request_route,
                payload,
                response.status,
                response.headers.get("x-credits-cost"),
                response.headers.get("x-credits-remaining"),
            )
    except HTTPError as error:
        raise FomoApiError(error.code, request_route) from None
    except (URLError, TimeoutError, json.JSONDecodeError) as error:
        raise RuntimeError("Fomo API request failed for {} ({})".format(request_route, type(error).__name__)) from None


def get_leaderboard(api_key, period="30d", limit=50):
    if period not in ("24h", "7d", "30d", "all"):
        raise ValueError("period must be one of: 24h, 7d, 30d, all")
    if limit < 1 or limit > 150 or (period == "all" and limit > 100):
        raise ValueError("limit is outside the documented leaderboard range")
    return get_json("/v2/leaderboard/{}".format(period), api_key, {"limit": limit})


def get_alerts(api_key, since=None, limit=100, alert_type=None, user_id=None, cursor=None):
    if not since and not cursor:
        raise ValueError("since or cursor is required for alert recovery")
    if limit < 1:
        raise ValueError("limit must be greater than zero")
    params = {"limit": limit}
    if since:
        params["since"] = since
    if alert_type:
        if alert_type not in ("buy", "sell", "thesis"):
            raise ValueError("alert_type must be one of: buy, sell, thesis")
        params["type"] = alert_type
    if user_id:
        params["userId"] = user_id
    if cursor:
        params["cursor"] = cursor
    return get_json("/v2/alerts", api_key, params)


def get_user_theses(api_key, user_id, limit=100, sort="recent", chain=None):
    """Historical user post read; returned list does not establish lifetime completeness."""
    if not isinstance(user_id, str) or not user_id.strip():
        raise ValueError("A stable Fomo user ID or handle is required")
    if limit < 1 or limit > 100:
        raise ValueError("limit must be between 1 and 100")
    if sort not in ("recent", "likes"):
        raise ValueError("sort must be recent or likes")
    params = {"limit": limit, "sort": sort}
    if chain is not None:
        params["chain"] = str(chain)
    return get_json("/v2/thesis/user/" + quote(user_id.strip(), safe=""), api_key, params)
