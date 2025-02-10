import subprocess

def get_saved_wifi_passwords():
    # Run the command to get all Wi-Fi profiles saved on the system
    wifi_profiles_command = ["netsh", "wlan", "show", "profiles"]
    try:
        wifi_profiles_output = subprocess.check_output(wifi_profiles_command, encoding="utf-8")
    except subprocess.CalledProcessError as e:
        print("Failed to retrieve Wi-Fi profiles. Ensure you are running as administrator.")
        return

    # Extract profile names from the output
    profiles = []
    for line in wifi_profiles_output.split("\n"):
        if "All User Profile" in line:
            profile_name = line.split(":")[1].strip()
            profiles.append(profile_name)

    if not profiles:
        print("No Wi-Fi profiles found.")
        return

    # For each profile, get the password (if available)
    wifi_passwords = {}
    for profile in profiles:
        wifi_password_command = ["netsh", "wlan", "show", "profile", profile, "key=clear"]
        try:
            wifi_password_output = subprocess.check_output(wifi_password_command, encoding="utf-8")
            password = None
            for line in wifi_password_output.split("\n"):
                if "Key Content" in line:
                    password = line.split(":")[1].strip()
                    break
            wifi_passwords[profile] = password if password else "No password found or network is open"
        except subprocess.CalledProcessError:
            # If the command fails, we can log or handle the error here
            wifi_passwords[profile] = "Failed to retrieve password (may require administrator privileges)"

    return wifi_passwords

if __name__ == "__main__":
    wifi_passwords = get_saved_wifi_passwords()
    
    if wifi_passwords:
        # Print the Wi-Fi profile names and their passwords
        for profile, password in wifi_passwords.items():
            print(f"Wi-Fi Profile: {profile}\nPassword: {password}\n")
