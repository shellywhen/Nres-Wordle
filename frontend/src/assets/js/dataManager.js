import d3 from 'd3'
let loadData = function (fname) {
  return d3.csv(fname)
}

export {
  loadData
}
