import { Component, Input } from '@angular/core';

@Component({
  selector: 'exemplar-toolbar',
  templateUrl: './toolbar.component.html',
  styleUrls: ['./toolbar.component.scss']
})
export class ExemplarToolbarComponent {
  @Input() mainContent: any;
}
