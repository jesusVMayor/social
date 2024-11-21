# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import date

from odoo.tests.common import TransactionCase


class TestMailActivityDoneMethods(TransactionCase):
    def setUp(self):
        super(TestMailActivityDoneMethods, self).setUp()
        activity_type = self.env["mail.activity.type"].search(
            [("name", "=", "Meeting")], limit=1
        )
        self.act1 = self.env["mail.activity"].create(
            {
                "activity_type_id": activity_type.id,
                "res_id": self.env.ref("base.res_partner_1").id,
                "res_model": "res.partner",
                "res_model_id": self.env["ir.model"]._get("res.partner").id,
                "user_id": self.env.user.id,
                "date_deadline": date.today(),
            }
        )
        self.act2 = self.env["mail.activity"].create(
            {
                "activity_type_id": activity_type.id,
                "res_id": self.env.ref("base.res_partner_1").id,
                "res_model": "res.partner",
                "res_model_id": self.env["ir.model"]._get("res.partner").id,
                "user_id": self.env.user.id,
                "date_deadline": date.today(),
            }
        )
        self.act2._action_done()

    def test_mail_activity_done(self):
        self.act1._action_done()
        self.assertTrue(self.act1.exists())
        self.assertEqual(self.act1.state, "done")

    def test_systray_get_activities(self):
        act_count = self.env.user.systray_get_activities()
        self.assertEqual(
            len(act_count), 1, "Number of activities should be equal to one"
        )

    def test_read_progress_bar(self):
        res_partner = self.env["res.partner"].browse(self.act1.res_model_id)
        params = {
            "domain": [],
            "group_by": "id",
            "progress_bar": {"field": "activity_state"},
        }
        result = res_partner._read_progress_bar(**params)
        self.assertEqual(result[0]["__count"], 1)

        self.act1._action_done()
        self.assertEqual(self.act1.state, "done")
        result = res_partner._read_progress_bar(**params)
        self.assertEqual(len(result), 0)

    def test_activity_state_search(self):
        today_activities = self.env["res.partner"].search(
            [("activity_state", "=", "today")]
        )
        self.assertEqual(len(today_activities), 1)
