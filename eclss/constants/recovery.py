"""
Recovery assumptions and equipment parameters.

Water recovery based on ISS WPA reference.
Equipment heat is an engineering estimate.
"""

# === Recovery Assumptions (closed-loop) ===

WATER_RECOVERY_EFFICIENCY = 0.93           # ISS WPA reference (~93%)
# ISS total water recovery with the Brine Processor Assembly added to the
# Urine Processor Assembly. NASA (2023), "NASA Achieves Water Recovery
# Milestone on International Space Station": 93-94% before the BPA, 98% after.
WATER_RECOVERY_EFFICIENCY_ISS_BPA = 0.98

# === Equipment ===

EQUIPMENT_HEAT_W_PER_CREW = 1_500.0        # assumption (1-2 kW/person)
