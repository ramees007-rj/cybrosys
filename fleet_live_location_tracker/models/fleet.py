from odoo import models, fields, api
import requests
import base64
import json


class Fleet(models.Model):
    """Inherit fleet.vehicle module to add two fields"""
    _inherit = 'fleet.vehicle'

    traccar_id = fields.Integer('Traccar ID')
    location_tracking = fields.Boolean('Location Tracking')

    def get_live_location(self):
        """To get live location based on the values in latitude and longitude fields"""
        return {
            'type': 'ir.actions.client',
            'tag': 'fleet_live_location',
        }

    @api.onchange('location_tracking')
    def _onchange_location_tracking(self):
        if self.location_tracking and not self.traccar_id:
            url = "https://demo2.traccar.org/api/devices"

            payload = json.dumps({
                "id": 0,
                "name": self.name,
                "uniqueId": self.name + "/" + str(self.id),
                "status": "",
                "disabled": "",
                "lastUpdate": fields.Datetime.now().isoformat(),
                "positionId": 0,
                "groupId": 0,
                "phone": "",
                "model": "",
                "contact": "",
                "category": "fleet",
                "geofenceIds": [
                    0
                ],
                "attributes": {}
            })
            headers = {
                'Authorization': 'Basic cmpAZ21haWwuY29tOjEyMzQ1',
                'Content-Type': 'application/json'
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            res = response.json()
            self.write({
                "traccar_id": res['id']
            })
