import { NgModule } from '@angular/core';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { CommonModule } from '@angular/common';
import { AnalysisComponent } from './analysis.component'
import { LineChartModule } from './line-chart/line-chart.module';
import { MatSliderModule } from '@angular/material/slider'
import { MatGridListModule } from '@angular/material/grid-list';
import { MatCardModule } from '@angular/material/card';
import {MatSnackBarModule} from '@angular/material/snack-bar';
import { RatingbarComponentModule, RatingbarComponent } from '@app/components'

@NgModule({
    imports: [
        CommonModule,
        BrowserAnimationsModule,
        LineChartModule,
        MatCardModule,
        MatSliderModule,
        MatGridListModule,
        MatSnackBarModule,
        RatingbarComponentModule
    ],
    declarations: [
        AnalysisComponent
    ],
    providers: [],
    bootstrap: [RatingbarComponent]
})
export class AnalysisModule { }