import json
from typing import List, Tuple
from components.batter import Batter
from requests import post, get


class CMS:
    def update_cms(self, batters: List[Batter]) -> None:
        """Update the CMS that holds all of the batter stats.

        Parameters:
            `batters` (List[Batter]): The batters to update."""
        # converts list of batters to json
        batters_json = [batter.to_dict() for batter in batters]

        # get necessary variables from config file
        endpoint, cms_auth_token, revalidate_token = self._get_config_variables()
        auth_header = self._get_auth_header(cms_auth_token)

        # update stats, publish, and revalidate the endpoint
        self._update_stats(endpoint, batters_json, auth_header)
        self._publish_stats(endpoint, auth_header)
        self._revalidate_endpoint(revalidate_token)

    def _get_config_variables(self) -> Tuple[str, str, str]:
        """Get the necessary variables from the config file.

        Returns:
            `Tuple[str, str, str]`: The endpoint, auth token, and revalidate token."""
        with open("credentials.json", "r") as json_file:
            credentials = json.load(json_file)
            endpoint = credentials["endpoint"]
            cms_auth_token = credentials["cms_auth_token"]
            revalidate_token = credentials["revalidate_token"]

        return endpoint, cms_auth_token, revalidate_token

    def _revalidate_endpoint(self, token: str) -> None:
        """Revalidate the endpoint from the NextJS api endpoint.

        Parameters:
            `token` (str): The revalidate token."""
        base_url = "https://mlb-hit-helper.vercel.app/api/revalidate?token="
        revalidate_token = token
        response = get(base_url + revalidate_token)
        print(response.json())

    def _get_auth_header(self, auth_token: str) -> dict:
        """Get the auth header.

        Parameters:
            `auth_token` (str): The auth token.

        Returns:
            `dict`: The auth header."""
        return {
            "Authorization": f"Bearer {auth_token}",
        }

    def _update_stats(self, endpoint: str, json: List[dict], header: dict) -> None:
        """Update the stats in the CMS via mutation.

        Parameters:
            `endpoint` (str): The endpoint.
            `json` (List[dict]): The batters json array to update.
            `header` (dict): The auth header."""
        updateMutation = """
            mutation updateJSON($json: Json!)  {
                updateBatting(
                    data: {stats: $json}, where: {id: "cl2v92aa4bxj80bipqgkw2t3d"}) {
                    id
                    stats
                }
            }"""

        post(endpoint, json={'query': updateMutation,
             'variables': {'json': json}}, headers=header)

    def _publish_stats(self, endpoint: str, header: dict) -> None:
        """Publish the stats in the CMS via mutation. This is done after
        the stats are updated.

        Parameters:
            `endpoint` (str): The endpoint.
            `header` (dict): The auth header."""
        publishMutation = """
        mutation publishJSON {
            publishBatting(where: {id: "cl2v92aa4bxj80bipqgkw2t3d"}, to:PUBLISHED) {
                id
            }
        }"""

        post(endpoint, json={"query": publishMutation}, headers=header)
