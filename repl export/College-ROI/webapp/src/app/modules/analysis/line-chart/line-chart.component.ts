import { Component, OnInit, ViewChild, Input, OnChanges } from '@angular/core';
import { ChartDataSets, ChartOptions } from 'chart.js';
import { Color, BaseChartDirective } from 'ng2-charts';
import { ElementRef, SimpleChange, SimpleChanges, Output, EventEmitter } from "@angular/core";
import { CalculatorService } from '@app/services/calculator.service'

@Component({
  selector: 'exemplar-line-chart',
  templateUrl: './line-chart.component.html',
  styleUrls: ['./line-chart.component.scss'],
  providers: [CalculatorService]
})
export class LineChartComponent implements OnInit, OnChanges{

  @Input() debtRepaymentPercent: number
  @Input() lineChartData: ChartDataSets[]
  @Input() age: string

  @Output() repaymentAgeEvent = new EventEmitter();
  debtRepaymentAge: string

  public lineChartLabels: String[] 
  public lineChartOptions: (ChartOptions & { annotation: any }) = {
    responsive: false,
    scales: {
      // We use this empty structure as a placeholder for dynamic theming.
      xAxes: [{
        ticks: {
          fontSize: 20,
          autoSkip: true,
          maxTicksLimit: 20
        },
        scaleLabel: {
          display: true,
          labelString: "Age",
          fontSize: 30
        }
      }],
      yAxes: [
        {

          id: 'y-axis-0',
          position: 'left',
          ticks: {
            fontSize: 25,
            callback: function(value, index, values) {
                return '$' + value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
            }
          },
          scaleLabel: {
            display: true,
            labelString: "Salary",
            fontSize: 30
          }
        }
      ],
    },
    annotation: {

      annotations: [
      ],
    },
    tooltips:{
      titleFontSize: 30,
      bodyFontSize: 30, 
      callbacks: {
        label: function(tooltipItem, data){
          return "$" + Number(tooltipItem.yLabel).toFixed(0).replace(/./g, function(c, i, a) {
            return i > 0 && c !== "." && (a.length - i) % 3 === 0 ? "," + c : c;
          });
        }
      }
    },
    legend:{
      labels: {fontSize: 22},
      cursor: "pointer",
      itemclick: function(e){
        e.ChartDataSeries.visible = true
        e.chart.render()
      }
    }
  };
  public lineChartColors: Color[] = [
    { // grey
      backgroundColor: 'rgba(159,159,151, 0.2)',
      borderColor: 'rgba(159,159,151,1)',
      pointBackgroundColor: 'rgba(159,159,151,1)',
      pointBorderColor: '#fff',
      pointRadius: 5,
      pointHoverRadius: 7,
      pointHoverBackgroundColor: '#fff',
      pointHoverBorderColor: 'rgba(159,159,151,0.8)'
    },
    { // purple
      backgroundColor: 'rgba(93,81,121,0.2)',
      borderColor: 'rgba(93,81,121,1)',
      pointBackgroundColor: 'rgba(93,81,121,1)',
      pointRadius: 5,
      pointHoverRadius: 7,
      pointBorderColor: '#fff',
      pointHoverBackgroundColor: '#fff',
      pointHoverBorderColor: 'rgba(93,81,121,1)'
    },
    { //teal 
      backgroundColor: 'rgba(136, 160, 150, 0.2)', 
      borderColor: 'rgba(136, 160, 150, 1)',
      pointBackgroundColor: 'rgba(136, 160, 150, 1)',
      pointRadius: 5,
      pointHoverRadius: 7,
      pointHoverBackgroundColor: '#fff',
      pointBorderColor: '#fff',
      pointHoverBorderColor: 'rgba(136, 160, 150, 0.8)'
    }, 
    { //tan 
      backgroundColor: 'rgba(187, 171, 139, 0.2)', 
      borderColor: 'rgba(187, 171, 139, 1)',
      pointBackgroundColor: 'rgba(187, 171, 139, 1)',
      pointRadius: 5,
      pointHoverRadius: 7,
      pointHoverBackgroundColor: '#fff',
      pointBorderColor: '#fff',
      pointHoverBorderColor: 'rgba(187, 171, 139, 0.8)'
    },
    { // coral
      backgroundColor: 'rgba(239,130,117,0.2)',
      borderColor: 'rgba(239,130,117,1)',
      pointBackgroundColor: 'rgba(239,130,117,1)',
      pointBorderColor: '#fff',
      pointRadius: 5,
      pointHoverRadius: 7,
      pointHoverBackgroundColor: '#fff',
      pointHoverBorderColor: 'rgba(239,130,117,0.8)'
    }
  ];
  public lineChartLegend = true;
  public lineChartType = 'line';

  @ViewChild(BaseChartDirective) chart: BaseChartDirective;

  constructor(private _calculatorService: CalculatorService) {
  }

  ngOnChanges(changes: SimpleChanges){
    for (let propName in changes){
      if(!changes.debtRepaymentPercent.isFirstChange()){     
        let amount = {repayment: changes.debtRepaymentPercent.currentValue}
        this._calculatorService.updateRepaymentPercentage(amount).subscribe()
        const calcObservable = this._calculatorService.getLineChartData()
        calcObservable.subscribe((data: any[]) => {
  
           this.lineChartData[4]={ 
             data: JSON.parse(data['repayment']), 
             label: 'Repayment Timeline',
             backgroundColor: 'rgba(239,130,117,0.2)',
             borderColor: 'rgba(239,130,117,1)',
             pointRadius: 5,
             pointHoverRadius: 7,
             pointBackgroundColor: 'rgba(239,130,117,1)',
             pointBorderColor: '#fff',
             pointHoverBackgroundColor: '#fff',
             pointHoverBorderColor: 'rgba(239,130,117,0.8)'
           }
           this.chart.chart.data.datasets[4] = this.lineChartData[4]
           this.chart.chart.update()
           this.debtRepaymentAge = JSON.parse(data['repayment']).findIndex(this.getRepaymentIndex) + this.age
           console.log("In child", this.debtRepaymentAge)
           this.repaymentAgeEvent.emit(this.debtRepaymentAge)
        })

      }
    }
  }

  ngOnInit() {
    this.lineChartLabels = this.generateLabels()
  }

  getRepaymentIndex(element){
    return element == 0
  }

  public generateLabels(){
    let age = parseInt(this.age)
    let labels = []
    for(let i = age; i < 65; i++){
      labels.push(String(i))
    }
    return labels
  }

}
