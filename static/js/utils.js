// utils.js

// Duplicate paths to make them appear on side maps when zooming out
function duplicatePath(path) {
    const duplicatedPaths = [];
    for (let i = -1; i <= 1; i++) {
        for (let j = -1; j <= 1; j++) {
            duplicatedPaths.push(path.map(([lat, lon]) => [lat, lon + 360 * j]));
            }
    }
    return duplicatedPaths;
}
