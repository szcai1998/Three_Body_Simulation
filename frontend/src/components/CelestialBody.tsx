import { useRef, useMemo } from 'react'
import { useFrame } from '@react-three/fiber'
import { TransformControls } from '@react-three/drei'
import * as THREE from 'three'
import { useSimulationStore } from '../store/useSimulationStore'
import type { Body } from '../store/useSimulationStore'

interface CelestialBodyProps {
  body: Body
  isGhost?: boolean
}

export function CelestialBody({ body, isGhost = false }: CelestialBodyProps) {
  const meshRef = useRef<THREE.Mesh>(null)
  
  const visualRadius = Math.max(0.1, Math.min(3.0, Math.pow(body.mass, 1/3) * 0.2))
  const mainColor = isGhost ? '#ef4444' : '#3b82f6'
  const glowColor = isGhost ? '#f87171' : '#60a5fa'
  
  // Debug log
  console.log('Rendering body:', body.id, body.position.components)
  
  const trailGeometry = useMemo(() => new THREE.BufferGeometry(), [])
  const trailMaterial = useMemo(() => new THREE.LineBasicMaterial({
    color: isGhost ? 0xef4444 : 0x60a5fa,
    transparent: true,
    opacity: isGhost ? 0.3 : 0.6,
    blending: THREE.AdditiveBlending,
    depthWrite: false
  }), [isGhost])


  useFrame(() => {
    if (meshRef.current) {
      meshRef.current.position.set(...body.position.components)
    }
    
    if (body.trail && body.trail.length > 1) {
      const positions = new Float32Array(body.trail.length * 3)
      for (let i = 0; i < body.trail.length; i++) {
        positions[i * 3] = body.trail[i].components[0]
        positions[i * 3 + 1] = body.trail[i].components[1]
        positions[i * 3 + 2] = body.trail[i].components[2]
      }
      trailGeometry.setAttribute('position', new THREE.BufferAttribute(positions, 3))
    }
  })

  const speedSq = body.velocity.components[0]**2 + body.velocity.components[1]**2 + body.velocity.components[2]**2
  const speed = Math.sqrt(speedSq)
  const emissiveIntensity = isGhost ? 0.5 : (1.0 + Math.min(speed * 0.5, 4.0))

  const { selectedBodyId, setSelectedBodyId, editMode } = useSimulationStore()
  const isSelected = selectedBodyId === body.id

  const meshContent = (
    <mesh 
      ref={meshRef} 
      position={new THREE.Vector3(...body.position.components)}
      onClick={(e) => {
        e.stopPropagation()
        setSelectedBodyId(body.id)
      }}
      onPointerOver={(e) => {
        e.stopPropagation()
        document.body.style.cursor = 'pointer'
      }}
      onPointerOut={() => {
        document.body.style.cursor = 'auto'
      }}
    >
      <sphereGeometry args={[visualRadius, 32, 32]} />
      <meshStandardMaterial 
        color={mainColor}
        emissive={glowColor}
        emissiveIntensity={isSelected ? emissiveIntensity * 2 : emissiveIntensity} 
        toneMapped={false}
        transparent={isGhost}
        opacity={isGhost ? 0.5 : 1.0}
      />
      {!isGhost && (
        <mesh>
          <sphereGeometry args={[visualRadius * 1.5, 32, 32]} />
          <meshBasicMaterial 
            color={mainColor}
            transparent 
            opacity={0.2} 
            blending={THREE.AdditiveBlending}
            depthWrite={false}
          />
        </mesh>
      )}
    </mesh>
  )

  return (
    <group>
      {isSelected && editMode && !isGhost ? (
        <TransformControls 
          mode="translate" 
          {...{
            onDraggingChanged: async (e: any) => {
              if (!e?.value && meshRef.current) {
                const pos = meshRef.current.position
                const { api } = await import('../services/api')
                await api.updateBody(body.id, { position: { components: [pos.x, pos.y, pos.z] } })
              }
            }
          }}
        >
          {meshContent}
        </TransformControls>
      ) : (
        meshContent
      )}
      
      {body.trail.length > 1 && (
        <primitive object={new THREE.Line(trailGeometry, trailMaterial)} />
      )}
    </group>
  )
}
