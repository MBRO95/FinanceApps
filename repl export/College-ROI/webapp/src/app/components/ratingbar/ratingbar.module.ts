import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { RatingbarComponent } from './ratingbar.component';

import {NgbModule} from '@ng-bootstrap/ng-bootstrap';


@NgModule({
  imports: [
    CommonModule,
    RouterModule,
    NgbModule
  ],
  declarations: [RatingbarComponent],
  exports: [RatingbarComponent]
})
export class RatingbarComponentModule { }
