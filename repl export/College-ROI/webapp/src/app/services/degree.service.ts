import { Injectable } from '@angular/core'
import { State } from './models/state'
import { College } from './models/college'
import { Degree } from './models/degree'

@Injectable()
export class DataService {

    getStates() {
        return [
            new State('AL', 'Alabama'),
            new State('AK', 'Alaska'),
            new State('AZ', 'Arizona'),
            new State('AR', 'Arkansas'),
            new State('CA', 'California'),
            new State('CO', 'Colorado'),
            new State('CT', 'Connecticut'),
            new State('DE', 'Delaware'),
            new State('FL', 'Florida'),
            new State('GA', 'Georgia'),
            new State('HI', 'Hawaii'),
            new State('ID', 'Idaho'),
            new State('IL', 'Illinois'),
            new State('IN', 'Indiana'),
            new State('IA', 'Iowa'),
            new State('KS', 'Kansas'),
            new State('KY', 'Kentucky'),
            new State('LA', 'Louisiana'),
            new State('ME', 'Maine'),
            new State('MD', 'Maryland'),
            new State('MA', 'Massachusetts'),
            new State('MI', 'Michigan'),
            new State('MN', 'Minnesota'),
            new State('MS', 'Mississippi'),
            new State('MO', 'Missouri'),
            new State('MT', 'Montana'),
            new State('NE', 'Nebraska'),
            new State('NV', 'Nevada'),
            new State('NH', 'New Hampshire'),
            new State('NJ', 'New Jersey'),
            new State('NM', 'New Mexico'),
            new State('NY', 'New York'),
            new State('NC', 'North Carolina'),
            new State('ND', 'North Dakota'),
            new State('OH', 'Ohio'),
            new State('OK', 'Oklahoma'),
            new State('OR', 'Oregon'),
            new State('PA', 'Pennsylvania'),
            new State('RI', 'Rhode Island'),
            new State('SC', 'South Carolina'),
            new State('SD', 'South Dakota'),
            new State('TN', 'Tennessee'),
            new State('TX', 'Texas'),
            new State('UT', 'Utah'),
            new State('VT', 'Vermont'),
            new State('VA', 'Virginia'),
            new State('WA', 'Washington'),
            new State('WV', 'West Virginia'),
            new State('WI', 'Wisconsin'),
            new State('WY', 'Wyoming'),
        ]
    }
}