import { Component, OnInit} from '@angular/core';
import { FormBuilder, FormGroup, Validators, FormControl } from '@angular/forms';
import { Observable } from 'rxjs/internal/Observable';
import { map, startWith } from 'rxjs/operators';

import { Router } from '@angular/router'


@Component({
  selector: 'exemplar-welcome',
  templateUrl: './welcome.component.html',
  styleUrls: ['./welcome.component.scss']
})

export class WelcomeComponent {

    constructor(private router: Router){}

    start(){
        this.router.navigateByUrl('/start')
    }

}
