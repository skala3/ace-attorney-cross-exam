"""
Case library with multiple test cases for Ace Attorney LLM system.
Each case has different scenarios and difficulty levels.
"""

from case_data import CaseData, Evidence, Contradiction


def create_sample_case() -> CaseData:
    """Original sample case - The Poisoned Coffee Mystery."""
    return CaseData(
        title="The Poisoned Coffee Mystery",
        description="A murder occurred at the law office. The defendant is accused of poisoning the victim's coffee.",
        victim="Victim Johnson",
        defendant="Secretary Smith",
        crime="Murder by poisoning",
        evidence_list=[
            Evidence(
                id="coffee_cup",
                name="Coffee Cup",
                description="A coffee cup found on the victim's desk. Contains traces of poison.",
            ),
            Evidence(
                id="security_log",
                name="Security Log",
                description="Building security log showing Secretary Smith entered at 9:00 AM, but the victim died at 8:30 AM.",
            ),
            Evidence(
                id="poison_bottle",
                name="Poison Bottle",
                description="Found in the defendant's desk drawer.",
            ),
            Evidence(
                id="witness_statement",
                name="Janitor's Statement",
                description="Janitor saw someone in a suit near the victim's office at 8:15 AM.",
            ),
        ],
        witness_name="Detective Williams",
        correct_solution=Contradiction(
            statement_id=1,
            evidence_id="security_log",
            explanation="The detective claims the defendant delivered coffee at 8:15 AM, but the security log shows she didn't arrive until 9:00 AM.",
        ),
        case_facts="""
        Ground Truth:
        - The real killer was actually the business partner who had access to the office keys
        - The partner entered at 8:15 AM (before security system was activated)
        - Secretary Smith arrived at 9:00 AM as usual
        - The poison bottle was planted in Smith's desk to frame her
        - The detective's testimony incorrectly states Smith delivered the coffee at 8:15 AM
        """,
    )


def create_theft_case() -> CaseData:
    """Case 2: The Museum Heist - A theft case."""
    return CaseData(
        title="The Stolen Diamond Case",
        description="A priceless diamond was stolen from the city museum during closing time.",
        victim="Museum Director",
        defendant="Night Guard Jackson",
        crime="Grand theft",
        evidence_list=[
            Evidence(
                id="security_footage",
                name="Security Camera Footage",
                description="Shows the alarm was disabled at 11:45 PM. The guard was supposedly on patrol until midnight.",
            ),
            Evidence(
                id="fingerprints",
                name="Fingerprint Report",
                description="Fingerprints on the display case belong to the defendant.",
            ),
            Evidence(
                id="patrol_log",
                name="Guard's Patrol Log",
                description="Guard's handwritten log shows he completed his 11:30 PM patrol route.",
            ),
            Evidence(
                id="diamond_replica",
                name="Replica Diamond",
                description="A fake diamond was left in place of the real one.",
            ),
        ],
        witness_name="Security Chief Martinez",
        correct_solution=Contradiction(
            statement_id=2,
            evidence_id="security_footage",
            explanation="The witness claims the guard was on patrol when the alarm was disabled at 11:45 PM, but the patrol log shows he finished his route at 11:30 PM.",
        ),
        case_facts="""
        Ground Truth:
        - The real thief was the museum curator who had override codes
        - The curator disabled the alarm at 11:45 PM
        - The guard's fingerprints were on the case because he cleaned it earlier that day
        - The guard was framed by planting evidence
        """,
    )


def create_accident_case() -> CaseData:
    """Case 3: The Traffic Accident - A vehicular manslaughter case."""
    return CaseData(
        title="The Hit and Run Mystery",
        description="A pedestrian was killed in a hit-and-run accident. The defendant's car was found at the scene.",
        victim="Pedestrian Lee",
        defendant="Driver Chen",
        crime="Vehicular manslaughter",
        evidence_list=[
            Evidence(
                id="car_damage",
                name="Vehicle Damage Report",
                description="The defendant's car has front-end damage consistent with hitting a person.",
            ),
            Evidence(
                id="phone_record",
                name="Phone Records",
                description="Show the defendant received a call at 10:05 PM on the night of the accident.",
            ),
            Evidence(
                id="traffic_camera",
                name="Traffic Camera Photo",
                description="Shows the defendant's car at the intersection at 10:15 PM. The accident occurred at 10:20 PM.",
            ),
            Evidence(
                id="eyewitness",
                name="Witness Statement",
                description="A nearby resident heard the crash at exactly 10:20 PM.",
            ),
        ],
        witness_name="Officer Rodriguez",
        correct_solution=Contradiction(
            statement_id=1,
            evidence_id="traffic_camera",
            explanation="The witness claims to have seen the defendant driving recklessly at 10:25 PM, but the traffic camera shows the car at the intersection at 10:15 PM, and it couldn't have moved after the 10:20 PM accident.",
        ),
        case_facts="""
        Ground Truth:
        - Someone stole the defendant's car earlier that evening
        - The defendant reported the car missing at 9:00 PM
        - The real driver was a car thief who crashed and fled
        - The defendant was at home when the accident occurred
        """,
    )


def create_arson_case() -> CaseData:
    """Case 4: The Warehouse Fire - An arson case."""
    return CaseData(
        title="The Warehouse Fire Case",
        description="A warehouse burned down, killing a night watchman. Arson is suspected.",
        victim="Watchman Brown",
        defendant="Business Owner Taylor",
        crime="Arson and murder",
        evidence_list=[
            Evidence(
                id="gas_can",
                name="Gasoline Can",
                description="Found near the warehouse with the defendant's fingerprints on it.",
            ),
            Evidence(
                id="fire_report",
                name="Fire Marshal Report",
                description="Fire started at 2:30 AM. Multiple points of origin detected.",
            ),
            Evidence(
                id="insurance_policy",
                name="Insurance Documents",
                description="Shows the defendant recently increased the warehouse insurance policy.",
            ),
            Evidence(
                id="alibis",
                name="Restaurant Receipt",
                description="Receipt from a 24-hour diner showing the defendant made a purchase at 2:45 AM, 30 miles away.",
            ),
        ],
        witness_name="Fire Investigator Jones",
        correct_solution=Contradiction(
            statement_id=2,
            evidence_id="alibis",
            explanation="The witness claims they saw the defendant fleeing the scene at 2:35 AM, but the receipt proves the defendant was 30 miles away at 2:45 AM. It's impossible to travel that distance in 10 minutes.",
        ),
        case_facts="""
        Ground Truth:
        - A business rival set the fire to eliminate competition
        - The rival planted the gas can with the defendant's fingerprints
        - The defendant was at the diner establishing an alibi (but for business fraud, not arson)
        - The witness mistook someone else for the defendant in the dark
        """,
    )


def get_all_cases() -> list[CaseData]:
    """Return all available test cases."""
    return [
        create_sample_case(),
        create_theft_case(),
        create_accident_case(),
        create_arson_case(),
    ]


def get_case_by_index(index: int) -> CaseData:
    """Get a specific case by index (0-3)."""
    cases = get_all_cases()
    if 0 <= index < len(cases):
        return cases[index]
    return create_sample_case()  # Default to first case
