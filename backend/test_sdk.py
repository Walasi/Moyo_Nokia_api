from backend.nokia_sdk import sdk_sim_swap_check, sdk_location_verify

print("Testing SIM Swap...")
sim_result = sdk_sim_swap_check("+3672123456")
print(sim_result)

print("Testing Location...")
loc_result = sdk_location_verify("+3672123456", lat=5.6037, lon=-0.1870)
print(loc_result)