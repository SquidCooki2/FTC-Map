import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import L, { Map as LeafletMap } from "leaflet";
import MarkerClusterGroup from "react-leaflet-cluster";
import { useEffect, useRef, useState } from "react";
import iconUrl from "leaflet/dist/images/marker-icon.png";
import iconShadow from "leaflet/dist/images/marker-shadow.png";
import "leaflet/dist/leaflet.css";

const DefaultIcon = L.icon({
  iconUrl,
  shadowUrl: iconShadow,
  iconSize: [25, 41],
  iconAnchor: [12, 41],
});

(L.Marker.prototype as any).options.icon = DefaultIcon;

type Team = {
  teamNumber: number;
  name: string;
  place: string;
  lat: number;
  lng: number;
  iconUrl?: string;
  website?: string;
};

export default function App() {
  const mapRef = useRef<LeafletMap | null>(null);
  const [teams, setTeams] = useState<Team[]>([]);

  useEffect(() => {
    fetch("teams_jittered.json")
      .then((res) => res.json())
      .then((data: Team[]) => setTeams(data))
      .catch((err) => console.error("Error loading team data:", err));
  }, []);

  

  return (
    <div className="full-screen">
      <MapContainer
        center={[20, 0]}
        zoom={2}
        ref={mapRef}
        style={{ height: "100%", width: "100%" }}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {/* Cluster group should wrap ALL markers */}
        <MarkerClusterGroup
          chunkedLoading
          maxClusterRadius={10}
        >
          {teams
            .map((team) => {
              const customIcon = team.iconUrl
                ? L.icon({
                    iconUrl: team.iconUrl,
                    iconSize: [32, 32],
                    iconAnchor: [16, 32],
                  })
                : DefaultIcon;

              return (
                <Marker
                  key={team.teamNumber}
                  position={[team.lat, team.lng]}
                  icon={customIcon}
                >
                  <Popup>
                    <div className="text-sm">
                      <strong>
                        {team.website ? (
                          <a href={team.website} target="_blank" rel="noopener noreferrer">
                            {team.name}
                          </a>
                        ) : (
                          team.name
                        )}
                      </strong>{" "}- {team.teamNumber}
                      <br />
                      {team.place}
                      <br />
                      <a
                        href={`https://ftcscout.org/teams/${team.teamNumber}`}
                        target="_blank"
                        rel="noopener noreferrer"
                      >
                        View on FTCScout
                      </a>
                    </div>
                  </Popup>
                </Marker>
              );
            })}
        </MarkerClusterGroup>
      </MapContainer>
    </div>
  );
}