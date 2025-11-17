from odoo import models, fields, api , _

class PriceList(models.Model):
    _name = 'price.list'
    _description = 'Price List'

    crm_inherit_id = fields.Many2one('crm.lead', string="CRM Reference", ondelete='cascade')

    name = fields.Char(string="Lift Name", readonly=True, copy=False, default=lambda self: _('New'))

    quantity = fields.Integer(string="Quantity", default=1)

    # Capacity
    capacity = fields.Integer(string="Capacity")
    capacity_amount = fields.Integer(string="Capacity Amount",compute="_compute_capacity_amount",readonly=True, copy=False,store=True)

    # Speed
    speed = fields.Selection([('1', '1'), ('1.5', '1.5'), ('1.75', '1.75')], string='Speed')
    speed_amount = fields.Integer(string="Speed Amount",compute="_compute_speed_amount",readonly=True, copy=False,store=True)

    # Stops
    stop = fields.Integer(string="No of Stops")
    stop_amount = fields.Integer(string="Stop Amount",compute="_compute_stop_amount",readonly=True, copy=False,store=True)

    # Door Opening
    door_opening = fields.Selection([
        ('seven', '700'),
        ('eight', '800'),
        ('nine', '900'),
        ('thousand', '1000'),
        ('hundred', '1100')
    ], string='Door Opening')
    door_opening_amount = fields.Integer(string="Door Opening Amount",compute="_compute_door_opening_amount",readonly=True, copy=False,store=True)

    # Additional Travel
    additional_travel = fields.Integer(string="Additional Travel")
    additional_travel_amount = fields.Integer(string="Additional Travel Amount",compute="_compute_additional_travel_amount",readonly=True, copy=False,store=True)

    # Base Price
    base_price = fields.Float(string="Base Price",compute="_compute_base_price", store=True,help='Sum of Capacity, Speed, No of Stops, Door Opening, Additional Travel')

    # Grand Total
    grand_total = fields.Float(string="Grand Total",compute="_compute_grand_total",store=True,readonly=True,help='Sum of Base price, Extras, Margin Percentage')

    extras = fields.Float(string="Extras",readonly=True,help='Sum of MRL, Cabin, Cabin(Extra for gold), Automatic Doors, Automatic Door(Extra for gold), Scaffolding, Door Height, License Cost, Free AMC, Storage, Other City')

    # Margin Percentage
    margin_grand_total = fields.Selection(
        [(str(i), f"{i}%") for i in range(1, 21)],
        string="Margin %",
        help="Select margin percentage (1% - 20%)"
    )

    # Margin Amount
    margin_amount = fields.Float(
        string="Margin Amount",
        compute="_compute_grand_total",
        store=True,
        readonly=True
    )

    # Base price tax id
    base_price_tax_id = fields.Many2one(
        'account.tax',
        string="Tax",
        domain=[('type_tax_use', '=', 'sale')],
    )

    # MRL
    mrl = fields.Integer(string="MRL", store=True)
    mrl_amount = fields.Integer(string="MRL",compute="_compute_mrl_amount", store=True)

    # Cabin
    cabin = fields.Selection([
        ('SS 441', 'SS 441'),
        ('SS 304', 'SS 304'),
        ('SS Lenin/Honeycomb', 'SS Lenin/Honeycomb'),
    ], string='Cabin')
    cabin_amount = fields.Integer(string="Cabin Amount",compute="_compute_cabin_amount", store=True)
    cabin_extra_for_gold = fields.Selection([('Extra for Gold', 'Extra for Gold')], string='Cabin(Extra for Gold)')
    cabin_extra_for_gold_amount = fields.Integer(string="Cabin Extra for Gold Amount",compute="_compute_cabin_extra_for_gold_amount",
                                                  store=True)
    cabin_total_amount = fields.Integer(string="Cabin Total Amount",compute="_compute_cabin_total_amount", store=True)

    # Automatic Doors
    automatic_doors = fields.Selection([
        ('SS 441- All', 'SS 441- All'),
        ('SS 441- Lobby', 'SS 441- Lobby'),
        ('SS 304- All', 'SS 304- All'),
        ('SS 304- Lobby', 'SS 304- Lobby'),
        ('SS Lenin/Honeycomb All', 'SS Lenin/Honeycomb All'),
        ('SS 304- Framed Glass All', 'SS 304- Framed Glass All'),
    ], string='Automatic Doors')
    automatic_doors_amount = fields.Integer(string="Automatic Door Amount",compute="_compute_automatic_doors_amount",
                                            store=True)
    automatic_doors_extra_for_gold = fields.Selection([('Extra for Gold', 'Extra for Gold')],
                                                      string='Automatic Doors(Extra for Gold)')
    automatic_doors_extra_for_gold_amount = fields.Integer(string="Automatic Doors Extra for Gold Amount",compute="_compute_automatic_doors_extra_for_gold_amount",
                                                           store=True)
    automatic_doors_total_amount = fields.Integer(string="Automatic Doors Total Amount",compute="_compute_automatic_doors_total_amount",
                                                  store=True)

    # Scaffolding
    scaffolding = fields.Selection([
        ('By Cooper', 'By Cooper'),
        ('By Owner', 'By Owner'),
    ], string='Scaffolding')
    scaffolding_amount = fields.Integer(string="Scaffolding Amount",compute="_compute_scaffolding_amount",  store=True)

    # Door Height
    door_height = fields.Char(string="Door Height", default=2100)
    door_height_amount = fields.Integer(string="Door Height Amount",compute="_compute_door_height_amount", store=True)

    # License
    license_amount = fields.Integer(string="License Cost", default=30000, readonly=True, copy=False)

    # Free AMC
    free_amc_amount = fields.Integer(string="Free AMC",compute="_compute_free_amc_amount", store=True)

    # Storage
    storage = fields.Selection([
        ('By Cooper', 'By Cooper'),
        ('By Owner', 'By Owner'),
    ], string='Storage')
    storage_amount = fields.Integer(string="Storage Amount",compute="_compute_storage_amount", store=True)

    # Other City
    other_city = fields.Char(string="Other City")
    other_city_amount = fields.Integer(string="Other City Amount",compute="_compute_other_city_amount", store=True)

    # Technical Specification

    type_of_lift_one_ids = fields.Many2many(
        'lift.type',
        'crm_lead_lift_type_rel',
        'lead_id',
        'lift_type_id',
        string='Type of Lift Required'
    )
    type_of_lift_two_ids = fields.Many2many(
        'lift.type.two',
        'crm_lead_lift_type_two_rel',
        'lead_id',
        'lift_type_two_id',
        string='Type of Lift II Required'
    )

    no_of_stop_opening = fields.Char(string="No of Stop & Opening")
    type_of_door_opening = fields.Selection([
        ('manual', 'Manual'),
        ('automatic', 'Automatic'),
    ], string='Type of Door Opening')
    type_of_door_required_in_hoist_way = fields.Selection([
        ('imperforated', 'Imperforated'),
        ('center_opening', 'Center Opening'),
        ('telescopic', 'Telescopic'),
        ('swing', 'Swing'),
    ], string='Type of Door Required in Hoist Way')
    type_of_landing_door_finish_required_in_hoist_way = fields.Selection([
        ('m_s_powder_coated', 'M.S Powder Coated'),
        ('s_s__hairline_finish', 'S.S Hairline Finish'),
        ('pre_coated_finish', 'Pre-Coated Finish'),
        ('framed_glass', 'Framed Glass'),
        ('small_vision', 'Small Vision'),
    ], string='Type of Landing Door Finish Required in Hoist Way')
    type_of_cabin_door_finish_required_in_hoist_way = fields.Selection([
        ('m_s_powder_coated', 'M.S Powder Coated'),
        ('s_s__hairline_finish', 'S.S Hairline Finish'),
        ('pre_coated_finish', 'Pre-Coated Finish'),
        ('framed_glass', 'Framed Glass'),
        ('small_vision', 'Small Vision'),
    ], string='Type of Cabin Door Finish Required in Hoist Way')
    type_of_cabin_finish_required_in_hoist_way = fields.Selection([
        ('m_s_powder_coated', 'M.S Powder Coated'),
        ('s_s__hairline_finish', 'S.S Hairline Finish'),
        ('pre_coated_finish', 'Pre-Coated Finish'),
        ('framed_glass', 'Framed Glass'),
    ], string='Type of Cabin Finish Required in Hoist Way')
    lift_well_width = fields.Integer(string="Lift Well Dimension Width (mm)")
    lift_well_depth = fields.Integer(string="Lift Well Dimension Depth (WOP/AP) (mm)")

    lift_car_width = fields.Integer(string="Lift Car Size Width (mm)")
    lift_car_height = fields.Integer(string="Lift Car Size Depth (mm)")

    door_opening_width = fields.Integer(string="Door Opening Width (mm)")
    door_opening_height = fields.Integer(string="Door Opening Height (mm)")

    type_of_source = fields.Selection([
        ('direct_customer', 'Direct Customer'),
        ('existing_client', 'Existing Client'),
        ('md', 'MD'),
        ('gm', 'GM'),
        ('company_enquiry', 'Company Enquiry'),
    ], string='Type of Source')
    price = fields.Integer(string="Price")
    remarks = fields.Text(string="Remarks")
    site_status = fields.Char(string="Site Status")

    # Payment Terms

    payment_terms = fields.Selection([
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
    ], string='Payment Terms')
    payment_terms_type = fields.Selection([
        ('term_one', 'Payment Term I'),
        ('term_two', 'Payment Term II'),
    ], string="Payment Term Type")
    payment_terms_note = fields.Text(string="Payment Terms Note", compute="_compute_payment_terms_note", readonly=True)

    # Delivery and Installation Schedule

    delivery_schedule = fields.Selection([
        ('passenger_lift', 'Passenger Lift'),
        ('car_lift', 'Car Lift'),
        ('glass_lift', 'Glass Lift'),
    ], string='Delivery Schedule (Production Time)')
    delivery_schedule_week = fields.Text(string="Delivery Schedule Week",
                                         compute="_compute_delivery_schedule_week", readonly=True)
    installation_schedule = fields.Selection([
        ('up_to_ten_stops', 'Up to 10 stops'),
        ('up_to_twenty_stops', 'Up to 20 stops'),
        ('up_to_thirty_stops', 'Up to 30 stops'),
        ('up_to_fourty_stops', 'Up to 40 stops'),
        ('up_to_fifty_stops', 'Up to 50 stops'),
    ], string='Installation Schedule')
    installation_schedule_week = fields.Text(string="Installation Schedule Week",
                                             compute="_compute_installation_schedule_week", readonly=True)

    @api.model
    def create(self, vals):
        # Handle multiple record creation
        if isinstance(vals, list):
            for val in vals:
                if not val.get('name') or val.get('name') == _('New'):
                    crm_ref = self.env['crm.lead'].browse(val.get('crm_inherit_id')).name if val.get(
                        'crm_inherit_id') else 'CRM'
                    capacity = val.get('capacity', 0)
                    speed = val.get('speed', 0)
                    stops = val.get('stop', 0)
                    year = fields.Date.context_today(self).year
                    sequence = self.env['ir.sequence'].next_by_code('price.list') or '0000'
                    val['name'] = f"Residential Lift-Capacity-{capacity}-Speed-{speed}-Stop-{stops}"
            return super(PriceList, self).create(vals)

        # Handle single record creation
        if not vals.get('name') or vals.get('name') == _('New'):
            crm_ref = self.env['crm.lead'].browse(vals.get('crm_inherit_id')).name if vals.get(
                'crm_inherit_id') else 'CRM'
            capacity = vals.get('capacity', 0)
            speed = vals.get('speed', 0)
            stops = vals.get('stop', 0)
            year = fields.Date.context_today(self).year
            sequence = self.env['ir.sequence'].next_by_code('price.list') or '0000'
            vals['name'] = f"Residential Lift-Capacity-{capacity}-Speed-{speed}-Stop-{stops}"

        return super(PriceList, self).create(vals)

    @api.depends('capacity')
    def _compute_capacity_amount(self):
        for rec in self:
            if rec.capacity:
                if rec.capacity <= 10:
                    rec.capacity_amount = rec.capacity * 14000
                else:
                    rec.capacity_amount = (rec.capacity * 14000) + 150000
            else:
                rec.capacity_amount = 0

    @api.depends('speed')
    def _compute_speed_amount(self):
        for rec in self:
            if rec.speed:
                mapping = {
                    '1': 1,
                    '1.5': 1.5,
                    '1.75': 1.75,
                }
                rec.speed_amount = mapping.get(rec.speed, 0) * 26000
            else:
                rec.speed_amount = 0

    @api.depends('stop')
    def _compute_stop_amount(self):
        for rec in self:
            if rec.stop:
                if rec.stop <= 10:
                    rec.stop_amount = ((rec.stop - 1) * 50000) + 4000
                else:
                    rec.stop_amount = ((rec.stop - 1) * 50000) + ((rec.stop - 10) * 25000) + 4000
            else:
                rec.stop_amount = 0

    @api.depends('capacity', 'door_opening')
    def _compute_door_opening_amount(self):
        opening_map = {
            'seven': 700,
            'eight': 800,
            'nine': 900,
            'thousand': 1000,
            'hundred': 1100,
        }

        for rec in self:
            rec.door_opening_amount = 0

            if not rec.capacity or not rec.door_opening:
                continue

            opening_value = opening_map.get(rec.door_opening)

            # rules (same as your old logic)
            if rec.capacity in [6, 8, 9, 10]:
                if opening_value in [700, 800]:
                    rec.door_opening_amount = 0
                elif opening_value == 900:
                    rec.door_opening_amount = 20000
                elif opening_value == 1000:
                    rec.door_opening_amount = 40000
                elif opening_value == 1100:
                    rec.door_opening_amount = 60000

            elif rec.capacity == 13:
                if opening_value in [700, 800, 900]:
                    rec.door_opening_amount = 0
                elif opening_value == 1000:
                    rec.door_opening_amount = 20000
                elif opening_value == 1100:
                    rec.door_opening_amount = 40000

            elif rec.capacity == 15:
                if opening_value in [700, 800, 900, 1000]:
                    rec.door_opening_amount = 0
                elif opening_value == 1100:
                    rec.door_opening_amount = 20000

    @api.depends('additional_travel')
    def _compute_additional_travel_amount(self):
        for rec in self:
            rec.additional_travel_amount = rec.additional_travel * 6000 if rec.additional_travel else 0

    # Base Price (only main calculation)
    @api.depends(
        'capacity_amount',
        'speed_amount',
        'stop_amount',
        'door_opening_amount',
        'additional_travel_amount',
        'capacity',
        'stop'
    )
    def _compute_base_price(self):
        for rec in self:
            total = (
                    rec.capacity_amount +
                    rec.speed_amount +
                    rec.stop_amount +
                    rec.door_opening_amount +
                    rec.additional_travel_amount
            )

            base = 0
            if rec.capacity and rec.stop:
                if rec.capacity > 11 and rec.stop > 10:
                    base = total + ((rec.stop - 10) * 5000)
                else:
                    base = total + 450000

            rec.base_price = base if base > 0 else 0

            print(f"Base Price for {rec.name}: {rec.base_price}")

    @api.depends('capacity')
    def _compute_mrl_amount(self):
        for rec in self:
            if rec.capacity:
                rec.mrl_amount = rec.capacity * 5000
            else:
                rec.mrl_amount = 0

    @api.depends('cabin', 'capacity')
    def _compute_cabin_amount(self):
        for rec in self:
            amount = 0
            if rec.cabin and rec.capacity:
                if rec.cabin == 'SS 441':  # SS 441
                    amount = (rec.capacity * 3500) + 20000 if rec.capacity < 11 else rec.capacity * 3500
                elif rec.cabin == 'SS 304':  # SS 304
                    amount = (rec.capacity * 6000) + 20000 if rec.capacity < 11 else rec.capacity * 6000
                elif rec.cabin == 'SS Lenin/Honeycomb':  # SS Lenin/Honeycomb
                    amount = (rec.capacity * 8500) + 20000 if rec.capacity < 11 else rec.capacity * 8500
            rec.cabin_amount = amount

    @api.depends('cabin_extra_for_gold', 'capacity')
    def _compute_cabin_extra_for_gold_amount(self):
        for rec in self:
            extra_amount = 0
            if rec.cabin_extra_for_gold == 'Extra for Gold' and rec.capacity:
                extra_amount = (rec.capacity * 8500) + 20000 if rec.capacity < 11 else rec.capacity * 8500
            rec.cabin_extra_for_gold_amount = extra_amount

    @api.depends('cabin_amount', 'cabin_extra_for_gold_amount')
    def _compute_cabin_total_amount(self):
        for rec in self:
            rec.cabin_total_amount = (rec.cabin_amount or 0) + (rec.cabin_extra_for_gold_amount or 0)

    @api.depends('automatic_doors', 'stop')
    def _compute_automatic_doors_amount(self):
        for rec in self:
            amount = 0
            stops = rec.stop if rec.stop else 1

            if rec.automatic_doors == 'SS 441- All':  # SS 441- All
                amount = stops * 5000
            elif rec.automatic_doors == 'SS 441- Lobby':  # SS 441- Lobby
                amount = 5900
            elif rec.automatic_doors == 'SS 304- All':  # SS 304- All
                amount = stops * 10000
            elif rec.automatic_doors == 'SS 304- Lobby':  # SS 304- Lobby
                amount = 10000
            elif rec.automatic_doors == 'SS Lenin/Honeycomb All':  # SS Lenin/Honeycomb All
                amount = stops * 17000
            elif rec.automatic_doors == 'SS 304- Framed Glass All':  # SS 304- Framed Glass All
                amount = stops * 18000

            rec.automatic_doors_amount = amount

    @api.depends('automatic_doors_extra_for_gold', 'stop')
    def _compute_automatic_doors_extra_for_gold_amount(self):
        for rec in self:
            extra_amount = 0
            stops = rec.stop if rec.stop else 1

            if rec.automatic_doors_extra_for_gold == 'Extra for Gold':
                extra_amount = stops * 15000

            rec.automatic_doors_extra_for_gold_amount = extra_amount

    @api.depends('automatic_doors_amount', 'automatic_doors_extra_for_gold_amount')
    def _compute_automatic_doors_total_amount(self):
        for rec in self:
            rec.automatic_doors_total_amount = (rec.automatic_doors_amount or 0) + (
                    rec.automatic_doors_extra_for_gold_amount or 0)

    @api.depends('scaffolding', 'stop')
    def _compute_scaffolding_amount(self):
        for rec in self:
            if rec.scaffolding == 'By Cooper':  # By Cooper
                if rec.stop and rec.stop > 10:
                    rec.scaffolding_amount = rec.stop * 3000
                else:
                    rec.scaffolding_amount = 10000
            elif rec.scaffolding == 'By Owner':  # By Owner
                rec.scaffolding_amount = 0
            else:
                rec.scaffolding_amount = 0

    @api.depends('stop')
    def _compute_door_height_amount(self):
        for rec in self:
            rec.door_height_amount = rec.stop * 2000 if rec.stop else 0

    @api.depends('license')
    def _compute_license_amount(self):
        for rec in self:
            rec.license_amount = 30000

    @api.depends('base_price')
    def _compute_free_amc_amount(self):
        for rec in self:
            rec.free_amc_amount = rec.base_price * 0.04 if rec.base_price else 0

    @api.depends('storage', 'stop')
    def _compute_storage_amount(self):
        for rec in self:
            if rec.storage == 'By Cooper':  # By Cooper
                if rec.stop and rec.stop <= 10:
                    rec.storage_amount = 20000
                elif rec.stop and rec.stop > 10:
                    rec.storage_amount = 20000 + (rec.stop - 10) * 1000
                else:
                    rec.storage_amount = 20000
            elif rec.storage == 'By Owner':  # By Owner
                rec.storage_amount = 0
            else:
                rec.storage_amount = 0

    @api.depends('other_city')
    def _compute_other_city_amount(self):
        for rec in self:
            rec.other_city_amount = 40000 if rec.other_city else 0

    # Grand Total (base_price + extras)
    @api.depends(
        'base_price',
        'mrl_amount',
        'cabin_amount',
        'cabin_extra_for_gold_amount',
        'automatic_doors_amount',
        'automatic_doors_extra_for_gold_amount',
        'scaffolding_amount',
        'door_height_amount',
        'license_amount',
        'free_amc_amount',
        'storage_amount',
        'other_city_amount',
        'margin_grand_total'
    )
    def _compute_grand_total(self):
        for rec in self:
            extras = (
                    rec.mrl_amount +
                    rec.cabin_amount +
                    rec.cabin_extra_for_gold_amount +
                    rec.automatic_doors_amount +
                    rec.automatic_doors_extra_for_gold_amount +
                    rec.scaffolding_amount +
                    rec.door_height_amount +
                    rec.license_amount +
                    rec.free_amc_amount +
                    rec.storage_amount +
                    rec.other_city_amount
            )

            rec.extras = extras

            base_total = rec.base_price + extras

            # margin calculation
            margin_val = float(rec.margin_grand_total) if rec.margin_grand_total else 0.0
            rec.margin_amount = (base_total * margin_val) / 100 if base_total else 0.0

            # final grand total (with margin included)
            rec.grand_total = base_total + rec.margin_amount

            # Debug print
            print(f"\n=== Lift: {rec.name} ===")
            print(f"Base Grand Total (Without Margin): {base_total}")
            print(f"Margin %: {margin_val}%")
            print(f"Margin Amount: {rec.margin_amount}")
            print(f"Final Grand Total (With Margin): {rec.grand_total}")

    @api.depends('payment_terms', 'payment_terms_type')
    def _compute_payment_terms_note(self):
        for rec in self:
            note = ""

            if rec.payment_terms == 'residential':
                if rec.payment_terms_type == 'term_one':
                    note = (
                        "Residential - Payment Term I:\n"
                        "30% advance at Signing Document.\n"
                        "20% along with Approval of Drawing.\n"
                        "45% towards request of materials (supply within 45 days).\n"
                        "5% on completion and handover."
                    )
                elif rec.payment_terms_type == 'term_two':
                    note = (
                        "Residential - Payment Term II:\n"
                        "35% advance at Signing Document.\n"
                        "25% along with Approval of Drawing.\n"
                        "35% towards request of materials (supply within 45 days).\n"
                        "5% on completion and handover."
                    )

            elif rec.payment_terms == 'commercial':
                if rec.payment_terms_type == 'term_one':
                    note = (
                        "Commercial - Payment Term I:\n"
                        "40% advance at Signing Document.\n"
                        "10% along with Approval of Drawing.\n"
                        "40% towards request of materials (supply within 45 days).\n"
                        "10% on completion and handover."
                    )
                elif rec.payment_terms_type == 'term_two':
                    note = (
                        "Commercial - Payment Term II:\n"
                        "50% advance at Signing Document.\n"
                        "20% along with Approval of Drawing.\n"
                        "20% towards request of materials (supply within 45 days).\n"
                        "10% on completion and handover."
                    )

            rec.payment_terms_note = note

    @api.depends('delivery_schedule')
    def _compute_delivery_schedule_week(self):
        for rec in self:
            if rec.delivery_schedule == 'passenger_lift':
                rec.delivery_schedule_week = "7 Weeks"
            elif rec.delivery_schedule == 'car_lift':
                rec.delivery_schedule_week = "13 Weeks"
            elif rec.delivery_schedule == 'glass_lift':
                rec.delivery_schedule_week = "15 Weeks"
            else:
                rec.delivery_schedule_week = ""

    @api.depends('installation_schedule')
    def _compute_installation_schedule_week(self):
        for rec in self:
            mapping = {
                'up_to_ten_stops': "5-6 Weeks",
                'up_to_twenty_stops': "9-10 Weeks",
                'up_to_thirty_stops': "11-12 Weeks",
                'up_to_fourty_stops': "13-14 Weeks",
                'up_to_fifty_stops': "15-16 Weeks",
            }
            rec.installation_schedule_week = mapping.get(rec.installation_schedule, "")






