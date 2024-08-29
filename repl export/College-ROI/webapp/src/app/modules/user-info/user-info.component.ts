import { Component, OnInit} from '@angular/core';
import { FormBuilder, FormGroup, Validators, FormControl } from '@angular/forms';
import { Observable } from 'rxjs/internal/Observable';
import { map, startWith } from 'rxjs/operators';

import { Router } from '@angular/router'

import { DataService } from '@app/services/dataservice'
import { CollegeService } from '@app/services/college.service'
import { DegreeService } from '@app/services/degree.service'
import { CalculatorService } from '@app/services/calculator.service'
import { UserService } from '@app/services/user.service'
import { State } from '@app/services/models/state'
import { College } from '@app/services/models/college'
import { Degree } from '@app/services/models/degree'
import { User } from '@app/services/models/user'

export interface Intents {
  value: string,
  viewValue: string
}

@Component({
  selector: 'exemplar-user-info',
  templateUrl: './user-info.component.html',
  styleUrls: ['./user-info.component.scss'],
  providers: [DataService, CollegeService, CalculatorService, DegreeService, UserService], 
})

export class UserInfoComponent implements OnInit {

  isLinear = false
  basicsFormGroup: FormGroup
  financeFormGroup: FormGroup
  collegeFormGroup: FormGroup

  all_college_data = {}
  states: State[]
  stateNames: string[] = []
  stabbrs: string [] = []
  colleges: string[] = []
  degrees: string[] = []

  filteredDegrees: Observable<string[]>;
  filteredColleges: Observable<string[]>;
  filteredStates: Observable<string[]>

  constructor(
    private _formBuilder: FormBuilder, 
    private router: Router, 
    private _dataService: DataService, 
    private _collegeService: CollegeService,
    private _calculatorService: CalculatorService,
    private _degreeService: DegreeService,
    private _userService: UserService
  ) {
    
    this.states = this._dataService.getStates()
    let names = []
    let stabbr = []
    this.states.forEach(function (name) {
      names.push(name.name)
      stabbr.push(name.id)
    })
    this.stabbrs = stabbr
    this.stateNames = names
  }
  

  ngOnInit() {
    this.basicsFormGroup = this._formBuilder.group({
      nameCtrl: ['', Validators.required],
      intentCtrl: ['', Validators.required],
      ageCtrl: ['', Validators.required],
      stateCtrl: ['', Validators.required]
    });
    this.financeFormGroup = this._formBuilder.group({
      loanCtrl: ['', Validators.required],
      scholarshipCtrl: ['', Validators.required]
    });
    this.collegeFormGroup = this._formBuilder.group({
      collegeCtrl: ['', Validators.required],
      degreeCtrl: ['', Validators.required]
    })

    const collegeObservable = this._collegeService.getColleges()
    collegeObservable.subscribe((collegeData: College[]) => {
      this.all_college_data = collegeData
      this.colleges = Object.values(collegeData['School Name'])
    })

    const degreeObservable = this._degreeService.getDegrees()
    degreeObservable.subscribe((degreeData: Degree[]) => {
      this.degrees = Object.values(degreeData['major'])
    })
    
    this.filteredDegrees = this.collegeFormGroup.get('degreeCtrl').valueChanges
      .pipe(
        startWith(''),
        map(value => this._filterDegrees(value))
      );

    this.filteredColleges = this.collegeFormGroup.get('collegeCtrl').valueChanges
      .pipe(
        startWith(''),
        map(value => this._filterColleges(value))
      )

    this.filteredStates = this.basicsFormGroup.get('stateCtrl').valueChanges
      .pipe(
        startWith(''),
        map(value => this._filterStates(value))
      )
  }

  private _filterDegrees(value: string): string[] {
    return this.degrees.filter(option => option.toLowerCase().includes(value.toLowerCase()));
  }

  private _filterColleges(value: string): string[] {
    return this.colleges.filter(option => option.toLowerCase().includes(value.toLowerCase()));
  }

  private _filterStates(value: string): string[] {
    return this.stateNames.filter(option => option.toLowerCase().includes(value.toLowerCase()))
  }

  intents: Intents[] = [
    { value: 'school-0', viewValue: 'Picked a school, need a major' },
    { value: 'degree-1', viewValue: 'Picked a major, need a school' },
    { value: 'both-2', viewValue: 'Have a school and a major' }
  ]

  saveBasics() {
    if (this.basicsFormGroup.value.intentCtrl == 'school-0') {
      this.collegeFormGroup.removeControl('degreeCtrl')
      this.collegeFormGroup.addControl('collegeCtrl', new FormControl('', Validators.required))
    }
    if (this.basicsFormGroup.value.intentCtrl == 'degree-1') {
      this.collegeFormGroup.removeControl('collegeCtrl')
      this.collegeFormGroup.addControl('degreeCtrl', new FormControl('', Validators.required))
    }
    if (this.basicsFormGroup.value.intentCtrl == 'both-2') {
      this.collegeFormGroup.addControl('collegeCtrl', new FormControl('', Validators.required))
      this.collegeFormGroup.addControl('degreeCtrl', new FormControl('', Validators.required))
    }

    let ageNum = Number(this.basicsFormGroup.value.ageCtrl)
    let age = {age: ageNum}
    this._calculatorService.setAge(age).subscribe()

    let name = { name: this.basicsFormGroup.value.nameCtrl}
    this._userService.setName(name).subscribe()
    
  }

  savePrinciple(){
    let total = Number(this.financeFormGroup.value.scholarshipCtrl)
    let principle = {principle: total}
    this._calculatorService.addPrinciple(principle).subscribe()
  }

  isSchoolInState(){
    let state = this.basicsFormGroup.value.stateCtrl
    let college = this.collegeFormGroup.value.collegeCtrl
    let idx = this.all_college_data['State'][this.colleges.indexOf(college)]
    return state === this.stateNames[this.stabbrs.indexOf(idx)]
  }

  onSubmit() {

    if(this.collegeFormGroup.value.collegeCtrl){
      let inState = {isInState: this.isSchoolInState()}
      let college = {college: this.collegeFormGroup.value.collegeCtrl}
      this._calculatorService.setIsInState(inState).subscribe()
      this._collegeService.setCollege(college).subscribe()
    } else {
      let college = {college: ''}
      this._collegeService.setCollege(college).subscribe()
    }
    
    if(this.collegeFormGroup.value.degreeCtrl){
      let degree = { degree: this.collegeFormGroup.value.degreeCtrl }
      this._degreeService.setDegree(degree).subscribe()
    } else {
      let degree = {degree: ''}
      this._degreeService.setDegree(degree).subscribe()
    }


    setTimeout(() => {
      this.router.navigate(['/result'])
    },1000)
    
  }


}
