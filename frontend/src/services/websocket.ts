import { useSimulationStore } from '../store/useSimulationStore'
import type { SimulationState } from '../store/useSimulationStore'

const WS_URL = 'ws://localhost:8000/ws/simulation'

class SimulationWebSocket {
  private ws: WebSocket | null = null
  private reconnectTimer: ReturnType<typeof setTimeout> | null = null
  private lastChartUpdate = 0
  private lastPhaseSpaceUpdate = 0
  private driftHistory: {time: number, drift: number, L_mag: number}[] = []
  private phaseSpaceHistory: {x: number, v: number}[] = []

  connect() {
    if (this.ws?.readyState === WebSocket.OPEN) return

    this.ws = new WebSocket(WS_URL)

    this.ws.onopen = () => {
      useSimulationStore.getState().setConnected(true)
      console.log('Simulation WebSocket connected')
    }

    this.ws.onmessage = (event) => {
      try {
        const state: Partial<SimulationState> = JSON.parse(event.data)
        const store = useSimulationStore.getState()
        
        if (state.time !== undefined) {
          if (state.time < this.lastChartUpdate) {
            this.driftHistory = []
            this.phaseSpaceHistory = []
            store.setChartData([])
            store.setPhaseSpaceData([])
            this.lastChartUpdate = state.time
            this.lastPhaseSpaceUpdate = state.time
          }
          
          if (state.time - this.lastChartUpdate > 0.5) {
            const l_mag = state.angular_momentum ? Math.sqrt(
              state.angular_momentum.components[0]**2 + 
              state.angular_momentum.components[1]**2 + 
              state.angular_momentum.components[2]**2
            ) : 0
            
            this.driftHistory.push({ 
              time: state.time, 
              drift: (state.energy_drift ?? 0) * 100,
              L_mag: l_mag
            })
            if (this.driftHistory.length > 50) this.driftHistory.shift()
            this.lastChartUpdate = state.time
            store.setChartData([...this.driftHistory])
          }

          if (state.time - this.lastPhaseSpaceUpdate > 0.1 && state.bodies && state.bodies.length > 0) {
            const body1 = state.bodies[0]
            this.phaseSpaceHistory.push({
              x: body1.position.components[0],
              v: body1.velocity.components[0]
            })
            if (this.phaseSpaceHistory.length > 200) this.phaseSpaceHistory.shift()
            this.lastPhaseSpaceUpdate = state.time
            store.setPhaseSpaceData([...this.phaseSpaceHistory])
          }
        }
        
        store.setSimulationState(state)
      } catch (err) {
        console.error('Failed to parse WebSocket message:', err)
      }
    }

    this.ws.onclose = () => {
      useSimulationStore.getState().setConnected(false)
      console.log('Simulation WebSocket disconnected. Reconnecting in 2s...')
      this.reconnectTimer = setTimeout(() => this.connect(), 2000)
    }

    this.ws.onerror = (err) => {
      console.error('Simulation WebSocket error:', err)
      this.ws?.close()
    }
  }

  disconnect() {
    if (this.reconnectTimer) clearTimeout(this.reconnectTimer)
    if (this.ws) {
      this.ws.onclose = null // Prevent auto-reconnect
      this.ws.close()
      this.ws = null
    }
    useSimulationStore.getState().setConnected(false)
  }

  sendCommand(command: 'start' | 'pause' | 'step') {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({ command }))
    }
  }
}

export const simulationWs = new SimulationWebSocket()
