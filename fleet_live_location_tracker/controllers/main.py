
from odoo import http
from odoo.http import request
import requests
from bs4 import BeautifulSoup
import base64


class MapView(http.Controller):
    """To view map view when clicking smart button based on respective latitude and longitude"""
    @http.route(['/location/<int:vehicle_id>', '/location/'], type='http')
    def redirect_map(self, vehicle_id=None):
        """This function is used to return to map with values for latitude and longitude"""
        server_url = request.env['ir.config_parameter'].sudo().get_param(
            'fleet.server_url')
        server_email = request.env['ir.config_parameter'].sudo().get_param(
            'fleet.traccar_email')
        server_password = request.env['ir.config_parameter'].sudo().get_param(
            'fleet.traccar_password')
        # endpoint = 'positions'
        endpoint = 'reports/route'
        credentials = f"{server_email}:{server_password}"
        encoded_credentials = base64.b64encode(
            credentials.encode("utf-8")).decode("utf-8")
        headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/json"
        }
        response = requests.get(server_url + endpoint+'?from=2023-03-12T13:52:00Z&to=2023-03-15T13:52:00Z', headers=headers)
        print("hhhh")
        S = BeautifulSoup(response.text, 'lxml')
        print(S)
        # if server_url and server_email and server_password:
        #     context = []
        #     if vehicle_id:
        #         query = f'?deviceId={vehicle_id}'
        #         response = requests.get(server_url + endpoint + query,
        #                                 headers=headers)
        #         response_data = response.json()
        #         for item in response_data:
        #             if item.get('deviceId') == vehicle_id:
        #                 context.append({
        #                     'deviceId': item.get('deviceId'),
        #                     'latitude': item.get('latitude'),
        #                     'longitude': item.get('longitude'),
        #                     'altitude': item.get('altitude'),
        #                     'speed': item.get('speed'),
        #                 })
        #                 break
        #     else:
        #         vehicle_ids = request.env['fleet.vehicle'].search([])
        #
        #         for item in vehicle_ids:
        #             flag = False
        #             if item.location_tracking:
        #                 for device in response_data:
        #                     if device.get('deviceId') == item.traccar_id:
        #                         flag = True
        #                         context.append({
        #                             'name': item.name,
        #                             'driver': item.driver_id.name,
        #                             'deviceId': item.get('deviceId'),
        #                             'latitude': item.get('latitude'),
        #                             'longitude': item.get('longitude'),
        #                             'altitude': item.get('altitude'),
        #                             'speed': item.get('speed'),
        #                         })
        #             else:
        #                 context.append({
        #                     'name': item.name,
        #                     'tracking': False
        #                 })
        #     return context
