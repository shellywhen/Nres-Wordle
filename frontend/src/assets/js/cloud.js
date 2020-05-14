/* eslint-disable */
import * as cloudGenerator from 'd3-cloud'
let svgId = 'basicCloudSvg'
let width = 900
let height = 500//$('svg').innerHeight()
console.log(width, height)
let testCloud = function (data) {
  let wordScale = d3.scaleLinear()
    .domain([0,75])
    .range([10,120])
  cloudGenerator()
      .size([width, height])
      .timeInterval(200)
      .words(data)
      .rotate(0) //function(d) { return 0 }
      .fontSize(d=>wordScale(d.frequency))
      .font('微软雅黑')
      //.fontStyle(function(d,i) { return fontSyle(Math.random()) })
      .fontWeight(['bold'])
      .text(function(d) { return d.text })
      .spiral('rectangular') // 'archimedean' or 'rectangular'
      .on('end', draw)
      .start()
}

function draw(words) {
  console.log(words, 'check data')
  d3.select('svg').append('g')
     .attr('class','wordcloud')
     .attr('transform', 'translate(' + width/2 + ',' + height/2 + ')')
     .selectAll('text')
      .data(words)
      .enter().append('text')
      .attr('class','word')
      .style('font-size', function(d) { return d.size + 'px' })
      .attr('text-anchor', 'middle')
      .attr('transform', function(d) { return 'translate(' + [d.x, d.y] + ')rotate(' + d.rotate + ')' })
      .text(function(d) { return d.text })
}

export {
  testCloud
}
