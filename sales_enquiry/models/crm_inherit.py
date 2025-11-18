from odoo import models, fields, api , _

class CrmInherit(models.Model):
    _inherit = 'crm.lead'

    price_list_ids = fields.One2many('price.list', 'crm_inherit_id',)
    sale_order_template_id= fields.Many2one("sale.order.template", string="Quotation Template")

    def action_sale_quotations_new(self):
        if not self.partner_id:
            return self.env["ir.actions.actions"]._for_xml_id("sale_crm.crm_quotation_partner_action")
        else:
            # Create Quotation
            sale_order = self.env['sale.order'].create({
                'partner_id': self.partner_id.id,
                'opportunity_id': self.id,
                'sale_order_template_id': self.sale_order_template_id.id,
            })

            lines = []

            # Loop lifts with index
            for idx, lift in enumerate(self.price_list_ids, start=1):
                # Lift label (I, II, III …)
                roman = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]
                lift_label = roman[idx - 1] if idx <= len(roman) else str(idx)

                # 👉 Section line
                lines.append({
                    'order_id': sale_order.id,
                    'display_type': 'line_section',
                    'name': f"Lift {lift_label}",
                })

                # Description
                description_parts = [f"Lift {lift_label} - Residential passenger lift"]
                extra_info = []
                if lift.name:
                    extra_info.append(f"capacity: {lift.name}")
                if lift.speed:
                    extra_info.append(f"speed: {lift.speed}")
                if lift.stop:
                    extra_info.append(f"stops: {lift.stop}")
                if extra_info:
                    description_parts.append(f"({', '.join(extra_info)})")
                description = " ".join(description_parts)

                # Base line
                price = (lift.grand_total)
                lines.append({
                    'order_id': sale_order.id,
                    'product_id': False,
                    'name': description,
                    'product_uom_qty': lift.quantity or 1,
                    'price_unit': price,
                    'tax_ids': [(6, 0, [lift.base_price_tax_id.id])] if lift.base_price_tax_id else [(6, 0, [])],
                })

                if lift.type_of_lift_one_ids:
                    type1_names = ", ".join(lift.type_of_lift_one_ids.mapped("name"))
                    description_parts.append(f"Type of Lift I: {type1_names}")

                if lift.type_of_lift_two_ids:
                    type2_names = ", ".join(lift.type_of_lift_two_ids.mapped("name"))
                    description_parts.append(f"Type of Lift II: {type2_names}")

                if lift.no_of_stop_opening:
                    description_parts.append(f"No of Stop & Opening: {lift.no_of_stop_opening}")

                if lift.type_of_door_opening:
                    description_parts.append(
                        f"Type of Door Opening: {dict(lift._fields['type_of_door_opening'].selection).get(lift.type_of_door_opening)}")

                if lift.type_of_door_required_in_hoist_way:
                    description_parts.append(
                        f"Type of Door Required in Hoist Way: {dict(lift._fields['type_of_door_required_in_hoist_way'].selection).get(lift.type_of_door_required_in_hoist_way)}")

                if lift.type_of_landing_door_finish_required_in_hoist_way:
                    description_parts.append(
                        f"Type of Landing Door Finish Required in Hoist Way: {dict(lift._fields['type_of_landing_door_finish_required_in_hoist_way'].selection).get(lift.type_of_landing_door_finish_required_in_hoist_way)}")

                if lift.type_of_cabin_door_finish_required_in_hoist_way:
                    description_parts.append(
                        f"Type of Cabin Door Finish Required in Hoist Way: {dict(lift._fields['type_of_cabin_door_finish_required_in_hoist_way'].selection).get(lift.type_of_cabin_door_finish_required_in_hoist_way)}")

                if lift.type_of_cabin_finish_required_in_hoist_way:
                    description_parts.append(
                        f"Type of Cabin Finish Required in Hoist Way: {dict(lift._fields['type_of_cabin_finish_required_in_hoist_way'].selection).get(lift.type_of_cabin_finish_required_in_hoist_way)}")

                if lift.lift_well_width:
                    description_parts.append(f"Lift Well Dimension Width (mm): {lift.lift_well_width}")

                if lift.lift_well_depth:
                    description_parts.append(f"Lift Well Dimension Depth (WOP/AP) (mm): {lift.lift_well_depth}")

                if lift.lift_car_width:
                    description_parts.append(f"Lift Car Size Width (mm): {lift.lift_car_width}")

                if lift.lift_car_height:
                    description_parts.append(f"Lift Car Size Depth (mm): {lift.lift_car_height}")

                if lift.door_opening_width:
                    description_parts.append(f"Door Opening Width (mm): {lift.door_opening_width}")

                if lift.door_opening_height:
                    description_parts.append(f"Door Opening Height (mm): {lift.door_opening_height}")

                if lift.type_of_source:
                    description_parts.append(
                        f"Type of Source: {dict(lift._fields['type_of_source'].selection).get(lift.type_of_source)}")

                if lift.price:
                    description_parts.append(f"Price: {lift.price}")

                if lift.remarks:
                    description_parts.append(f"Remarks: {lift.remarks}")

                if lift.site_status:
                    description_parts.append(f"Site Status: {lift.site_status}")

                if lift.payment_terms:
                    description_parts.append(
                        f"Payment Terms: {dict(lift._fields['payment_terms'].selection).get(lift.payment_terms)}")

                if lift.payment_terms_type:
                    description_parts.append(
                        f"Payment Terms Type: {dict(lift._fields['payment_terms_type'].selection).get(lift.payment_terms_type)}")

                if lift.payment_terms_note:
                    description_parts.append(f"Payment Terms Note: {lift.payment_terms_note}")

                if lift.delivery_schedule:
                    description_parts.append(
                        f"Delivery Schedule: {dict(lift._fields['delivery_schedule'].selection).get(lift.delivery_schedule)}")

                if lift.delivery_schedule_week:
                    description_parts.append(f"Delivery Schedule Week: {lift.delivery_schedule_week}")

                if lift.installation_schedule:
                    description_parts.append(
                        f"Installation Schedule: {dict(lift._fields['installation_schedule'].selection).get(lift.installation_schedule)}")

                if lift.installation_schedule_week:
                    description_parts.append(f"Installation Schedule Week: {lift.installation_schedule_week}")

            # Create all lines at once
            self.env['sale.order.line'].create(lines)

            return {
                'type': 'ir.actions.act_window',
                'res_model': 'sale.order',
                'view_mode': 'form',
                'res_id': sale_order.id,
            }