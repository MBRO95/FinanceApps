import { NgModule } from '@angular/core';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { CommonModule } from '@angular/common';
import { WelcomeComponent } from './welcome.component'

import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';

@NgModule({
    imports: [
        CommonModule,
        BrowserAnimationsModule,
        MatCardModule,
        MatButtonModule
    ],
    declarations: [
        WelcomeComponent
    ],
    providers: []
})
export class WelcomeModule { }
