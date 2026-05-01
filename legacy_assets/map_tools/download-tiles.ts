//https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames
import * as fs from 'fs';
import Axios from 'axios';
//import * as perf from 'perf_hooks';

function lon2tile(lon: number, zoom: number): number { return (Math.floor((lon + 180) / 360 * Math.pow(2, zoom))); }
function lat2tile(lat: number, zoom: number): number { return (Math.floor((1 - Math.log(Math.tan(lat * Math.PI / 180) + 1 / Math.cos(lat * Math.PI / 180)) / Math.PI) / 2 * Math.pow(2, zoom))); }

async function download(url: string, output: string) {
    try {
        const writer = fs.createWriteStream(output)

        const response = await Axios({
            url,
            method: 'GET',
            responseType: 'stream'
        });

        response.data.pipe(writer)
    } catch (e) {
        console.log(e.config.url);
        await download(url, output);
    }
}

function sleep(ms: number) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

interface TileRegion {
    top: number;
    left: number;
    bottom: number;
    right: number;
}

async function getTilesPizza(zoom: number, tile: TileRegion, overwrite: boolean) {
    const servers: string[] = ['a', 'b', 'c'];
    for (let htile = tile.left; htile <= tile.right; htile++) {
        const dirpath = `tiles/${zoom}/${htile}/`;
        fs.mkdirSync(dirpath, { recursive: true });
        const percenth = ((htile - tile.left) / (tile.right - tile.left)) * 100;
        console.log(dirpath + '\t\t\t' + percenth + '%');
        for (let vtile = tile.top; vtile <= tile.bottom; vtile++) {
            const path = `tiles/${zoom}/${htile}/${vtile}.png`;
            if (fs.existsSync(path) && !overwrite) {
                const stats = fs.statSync(path);
                if (stats["size"] > 0) continue;
                console.log('zero size ' + path); 
            }
            const s = servers[(Math.random() * 3) | 0];
            const url = `https://${s}.tile.openstreetmap.org/${zoom}/${htile}/${vtile}.png`;
            //const start = perf.performance.now();
            if (zoom == 19) console.log(`${vtile - tile.top}/${tile.bottom - tile.top}`);
            await download(url, path);
            //const time = perf.performance.now() - start;
            //console.log(time);
        }
    }
}

interface Region {
    north_edge: number;
    west_edge: number;
    south_edge: number;
    east_edge: number;
}

async function getTilesCake(min_zoom: number, max_zoom: number, r: Region, overwrite = false) {
    for (let zoom = min_zoom; zoom <= max_zoom; zoom++) {
        const tile: TileRegion = {
            top: lat2tile(r.north_edge, zoom),
            left: lon2tile(r.west_edge, zoom),
            bottom: lat2tile(r.south_edge, zoom),
            right: lon2tile(r.east_edge, zoom)
        }
        //{zoom}/{left}/{top}.png

        await getTilesPizza(zoom, tile, overwrite);
    }
}

//console.log(process.argv[2])
const regions: Region[] = [
    { //0 krai
        north_edge: 48.5,
        west_edge: 130.3,
        south_edge: 42.2,
        east_edge: 139.2
    },
    { //1 vlad
        north_edge: 43.22,
        west_edge: 131.83,
        south_edge: 41.22,
        east_edge: 131.99
    },
    { north_edge: 42.86740922288482, west_edge: 132.84187316894534, south_edge: 42.767178634023345, east_edge: 132.96752929687503 }, //2 nah
    { north_edge: 43.17513839170044, west_edge: 133.07464599609378, south_edge: 43.08393444692567, east_edge: 133.20304870605472 }, //3 part
    { north_edge: 43.84690817091638, west_edge: 131.8894958496094, south_edge: 43.731414013769, east_edge: 132.08862304687503 }, //4 ussur
    { north_edge: 43.38, west_edge: 132.05, south_edge: 43.32, east_edge: 132.24 }, //5 artem
    { north_edge: 43.49, west_edge: 132.21, south_edge: 43.33, east_edge: 132.33 }, //6 artem 2 
    { north_edge: 42,
      west_edge: 131.955,
      south_edge: 41.5,
      east_edge: 131.99
    }, //7
    { north_edge: 43.31243871434339, west_edge: 132.03609466552737, south_edge: 43.2472033773598, east_edge: 132.09171295166018 }, //8 trud
    { north_edge: 43.221877736705416, west_edge: 132.13351249694827, south_edge: 43.19998290281629, east_edge: 132.1714496612549 }, //9 emar
    { north_edge: 43.19923208343623, west_edge: 132.10381507873538, south_edge: 43.18596608428708, east_edge: 132.13179588317874 }, //10 lazur
    { north_edge: 43.16962992688607, west_edge: 132.33100891113284, south_edge: 43.09659586628848, east_edge: 132.40396499633792 }, //11 bolshoi kamen

];
getTilesCake(0, Number(process.argv[3]), regions[process.argv[2]]);
