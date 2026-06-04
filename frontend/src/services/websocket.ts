import { useSimulationStore } from '../store/useSimulationStore'
import type { SimulationState } from '../store/useSimulationStore'

const WS_URL = 'ws://localhost:8000/ws/simulation'

class SimulationWebSocket {
  private ws: WebSocket | null = null
  private reconnectTimer: ReturnType<typeof setTimeout> | null = null
  private lastChartUpdate = 0
  private driftHistory: {time: number, drift: number}[] = []

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
        
        if (state.time !== undefined && state.energy_drift !== undefined) {
          if (state.time < this.lastChartUpdate || state.time === 0) {
            this.driftHistory = []
            this.lastChartUpdate = 0
          }
          if (state.time - this.lastChartUpdate > 0.5) {
            this.driftHistory.push({ time: state.time, drift: state.energy_drift * 100 })
            if (this.driftHistory.length > 50) this.driftHistory.shift()
            this.lastChartUpdate = state.time
            store.setChartData([...this.driftHistory])
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
