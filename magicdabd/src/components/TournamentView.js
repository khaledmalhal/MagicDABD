import { SingleEliminationBracket, DoubleEliminationBracket, 
    Match, MATCH_STATES, SVGViewer } from '@g-loot/react-tournament-brackets';
import { partidas } from './Navbar.js';
import { useEffect, useState } from 'react';

function TournamentView() {
  const [matches, setMatches] = useState(null);

  useEffect(() => {
    console.log(partidas)
    let jugadores = []
    for (const partida of partidas) {
      let found = jugadores.some(el => el['jugador'] == partida['duelista1'])
      if (!found) {
        jugadores.push({jugador: partida['duelista1'], count: 1})
      } else {
        let index = jugadores.find(x => x['jugador'] == partida['duelista1'])
        jugadores[index]['count'] = jugadores[index]['count'] + 1
      }
      found = jugadores.some(el => el['jugador'] == partida['duelista2'])
      if (!found) {
        jugadores.push({jugador: partida['duelista2'], count: 1})
      } else {
        let index = jugadores.find(x => x['jugador'] == partida['duelista2'])
        jugadores[index]['count'] = jugadores[index]['count'] + 1
      }
    }
    jugadores.sort((a, b) => {
      if (a['count'] < b['count']) return -1;
      if (a['count'] > b['count']) return 1;
      return 0;
    })
    if (jugadores.length > 0) {
      for (let i = jugadores[0]['count']; i > 0; i--) {
        const rondaJugadores = jugadores.filter(x => x['count'] >= i)
        console.log(rondaJugadores)
        for (const jugador of rondaJugadores) {
          const index1 = partidas.find(x => x['duelista1'] == jugador['jugador'])
          // const duelista1 = 
          // const pair 
        }
      }
    }
  }, matches);

  return (
    <>
    {matches != null && (
      <SingleEliminationBracket
      matches={matches}
      matchComponent={Match}
      svgWrapper={({ children, ...props }) => (
        <SVGViewer width={500} height={500} {...props}>
          {children}
        </SVGViewer>
      )}
      />
    )}
    </>
  )
}

export default TournamentView;