import subprocess
import time

def disable_services():
    """Disables selected services."""
    services = [
        "bthserv",  # Bluetooth Support Service
        "lfsvc",  # Geolocation Service
        "TermService",  # Remote Desktop Services
        "RemoteAccess",  # Routing and Remote Access
        "WFDSConMgrSvc",  # Wi-Fi Direct Services
        "xbgm",  # Xbox Game Monitoring
        "LanmanServer"  # Default Share Status
    ]
    
    disabled_services = []
    failed_services = []
    
    for service in services:
        result = subprocess.run(["sc", "config", service, "start=", "disabled"], capture_output=True, text=True)
        if "SUCCESS" in result.stdout:
            disabled_services.append(service)
        else:
            failed_services.append(service)
    
    return disabled_services, failed_services

def enable_services():
    """Enables and starts selected services."""
    services = [
        "bthserv", "lfsvc", "TermService", "RemoteAccess", "WFDSConMgrSvc", "xbgm", "LanmanServer"
    ]

    enabled_services = []
    failed_services = []

    for service in services:
        try:
            # Step 1: Set to manual (or auto)
            config_result = subprocess.run(
                ["sc", "config", service, "start=", "auto"],
                capture_output=True,
                text=True,
                timeout=10
            )

            if "SUCCESS" not in config_result.stdout:
                failed_services.append(f"{service} (config failed)")
                continue

            # Step 2: Start service
            subprocess.run(
                ["sc", "start", service],
                capture_output=True,
                text=True,
                timeout=10
            )

            # Step 3: Wait and verify status
            for _ in range(5):
                time.sleep(1)
                status_check = subprocess.run(["sc", "query", service], capture_output=True, text=True)
                if "RUNNING" in status_check.stdout:
                    enabled_services.append(service)
                    break
            else:
                failed_services.append(f"{service} (didn't confirm running)")

        except Exception as e:
            failed_services.append(f"{service} (error: {e})")

    return enabled_services, failed_services

def stop_services():
    """Stops selected services silently with timeouts."""
    services = [
        "bthserv",
        "lfsvc",
        "TermService",
        "RemoteAccess",
        "WFDSConMgrSvc",
        "xbgm",
        "LanmanServer"
    ]

    stopped_services = []
    failed_services = []

    for service in services:
        query = subprocess.run(["sc", "query", service], capture_output=True, text=True)
        if "FAILED 1060" in query.stdout or "OpenService FAILED 1060" in query.stdout:
            failed_services.append(f"{service} (not found)")
            continue
        if "STOPPED" in query.stdout:
            continue

        result = subprocess.run(["sc", "stop", service], capture_output=True, text=True)

        if "FAILED 1051" in result.stdout:
            failed_services.append(f"{service} (has dependencies)")
        elif "STOP_PENDING" in result.stdout:
            for _ in range(5):
                time.sleep(2)
                recheck = subprocess.run(["sc", "query", service], capture_output=True, text=True)
                if "STOPPED" in recheck.stdout:
                    stopped_services.append(service)
                    break
            else:
                failed_services.append(f"{service} (timeout waiting to stop)")
        elif "STOPPED" in result.stdout or "successfully stopped" in result.stdout.lower():
            stopped_services.append(service)
        else:
            failed_services.append(f"{service} (unknown failure)")

    return stopped_services, failed_services

def check_services_status():
    services = {
        "bthserv": "Bluetooth Support Service",
        "lfsvc": "Geolocation Service",
        "TermService": "Remote Desktop Services",
        "RemoteAccess": "Routing and Remote Access",
        "WFDSConMgrSvc": "Wi-Fi Direct Services",
        "xbgm": "Xbox Game Monitoring",
        "LanmanServer": "Default Share Status"
    }

    statuses = {}

    for service, service_name in services.items():
        # First check config for DISABLED
        config_result = subprocess.run(["sc", "qc", service], capture_output=True, text=True)
        if "DISABLED" in config_result.stdout:
            statuses[service_name] = "Disabled"
            continue

        # Then check actual running/stopped state
        result = subprocess.run(["sc", "query", service], capture_output=True, text=True)
        
        if "RUNNING" in result.stdout:
            statuses[service_name] = "Running"
        elif "STOPPED" in result.stdout:
            statuses[service_name] = "Stopped"
        else:
            statuses[service_name] = "Unknown"

    return statuses


    return statuses
