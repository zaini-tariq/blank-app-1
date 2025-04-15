import streamlit as st
import random
import time

# --- Server Class ---
class Server:
    def __init__(self, name):
        self.name = name
        self.cpu = random.randint(10, 90)
        self.memory = random.randint(10, 90)
        self.disk = random.randint(10, 90)

    def status(self):
        return {
            "CPU": self.cpu,
            "Memory": self.memory,
            "Disk": self.disk
        }

    def is_healthy(self):
        return self.cpu < 80 and self.memory < 80 and self.disk < 90

    def apply_fix(self):
        self.cpu = max(0, self.cpu - random.randint(5, 20))
        self.memory = max(0, self.memory - random.randint(5, 20))
        self.disk = max(0, self.disk - random.randint(5, 20))

# --- Maintenance Agent Class ---
class MaintenanceAgent:
    def __init__(self, servers):
        self.servers = servers

    def monitor_and_act(self):
        logs = []
        for server in self.servers:
            logs.append(f"🔍 Checking {server.name}")
            status = server.status()
            for k, v in status.items():
                logs.append(f"   {k}: {v}%")

            if not server.is_healthy():
                logs.append("⚠️  Status: Unhealthy")
                server.apply_fix()
                logs.append("🛠️  Fixes applied.")
            else:
                logs.append("✅ Status: Healthy")
        return logs

    def all_servers_healthy(self):
        return all(server.is_healthy() for server in self.servers)

# --- Streamlit App ---
st.set_page_config(page_title="Autonomous Server Maintenance", layout="centered")
st.title("🤖 Autonomous Server Maintenance Agent")

if 'servers' not in st.session_state:
    st.session_state.servers = [Server(f"Server-{i+1}") for i in range(3)]
    st.session_state.agent = MaintenanceAgent(st.session_state.servers)
    st.session_state.round = 1
    st.session_state.logs = []

st.subheader("Current Maintenance Cycle")

if st.button("🧠 Run Maintenance Cycle"):
    logs = st.session_state.agent.monitor_and_act()
    st.session_state.logs.extend([f"**Cycle {st.session_state.round}:**"] + logs + ["---"])
    st.session_state.round += 1

if st.button("🔄 Restart"):
    st.session_state.clear()
    st.experimental_rerun()

# Display logs
for line in st.session_state.logs:
    st.markdown(line)

if st.session_state.agent.all_servers_healthy():
    st.success("🎉 Goal Achieved! All servers are now healthy.")
