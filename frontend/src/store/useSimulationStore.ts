import { create } from 'zustand'

export interface VectorN {
  components: [number, number, number]
}

export interface Body {
  id: string
  mass: number
  position: VectorN
  velocity: VectorN
  acceleration: VectorN
  trail: VectorN[]
}

export interface SimulationState {
  bodies: Body[]
  G: number
  epsilon: number
  time: number
  timestep: number
  integrator: "verlet" | "rk4" | "euler" | "kepler"
  running: boolean
  chaos_mode: boolean
  shadow_bodies: Body[] | null
  playback_speed: number
  
  initial_energy: number | null
  total_energy: number
  kinetic_energy: number
  potential_energy: number
  energy_drift: number
  angular_momentum: VectorN
  center_of_mass: VectorN
  min_distance: number
  divergence_history: number[]
}

export interface StoreState extends SimulationState {
  connected: boolean
  mode: 1 | 2 | 3
  selectedBodyId: string | null
  editMode: boolean
  playbackSpeed: number
  chartData: {time: number, drift: number, L_mag?: number}[]
  phaseSpaceData: {x: number, v: number}[]
  setConnected: (status: boolean) => void
  setSimulationState: (state: Partial<SimulationState>) => void
  setSelectedBodyId: (id: string | null) => void
  setEditMode: (mode: boolean) => void
  setMode: (mode: 1 | 2 | 3) => void
  setPlaybackSpeed: (speed: number) => void
  setChartData: (data: {time: number, drift: number, L_mag?: number}[]) => void
  setPhaseSpaceData: (data: {x: number, v: number}[]) => void
}

export const useSimulationStore = create<StoreState>((set) => ({
  bodies: [],
  G: 1.0,
  epsilon: 1e-3,
  time: 0.0,
  timestep: 0.01,
  integrator: "verlet",
  running: false,
  chaos_mode: false,
  shadow_bodies: null,
  playback_speed: 1,
  
  initial_energy: null,
  total_energy: 0.0,
  kinetic_energy: 0.0,
  potential_energy: 0.0,
  energy_drift: 0.0,
  angular_momentum: { components: [0, 0, 0] },
  center_of_mass: { components: [0, 0, 0] },
  min_distance: 0.0,
  divergence_history: [],

  connected: false,
  mode: 3,
  selectedBodyId: null,
  editMode: false,
  playbackSpeed: 1,
  chartData: [],
  phaseSpaceData: [],

  setConnected: (status) => set({ connected: status }),
  setSelectedBodyId: (id) => set({ selectedBodyId: id }),
  setEditMode: (mode) => set({ editMode: mode }),
  setSimulationState: (newState) => set((state) => ({ ...state, ...newState })),
  setMode: (mode) => set({ mode }),
  setPlaybackSpeed: (speed) => set({ playbackSpeed: speed }),
  setChartData: (data) => set({ chartData: data }),
  setPhaseSpaceData: (data) => set({ phaseSpaceData: data }),
}))
