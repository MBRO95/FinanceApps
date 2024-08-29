import { Component, Input, AfterViewInit } from '@angular/core';


@Component({
  selector: 'exemplar-ratingbar',
  templateUrl: './ratingbar.component.html',
  styleUrls: ['./ratingbar.component.scss']
})
export class RatingbarComponent {
  constructor() {}
  currentRate = 0;
}
