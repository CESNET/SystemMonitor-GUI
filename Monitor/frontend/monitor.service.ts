import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Observable, of } from 'rxjs';
import { catchError, map, tap } from 'rxjs/operators';

import { Pattern } from './common/pattern';

@Injectable({
  providedIn: 'root',
})
export class MonitorService {

  constructor(
    private http: HttpClient
  ) { }

  /** GET patterns and their names from backend */
  getPattenrs(): Observable<Pattern[]> {
    return this.http.get<Pattern[]>('/monitor/patterns').pipe(
      catchError(this.handleError('getPatterns', []))
    );
  }

  /**
   * Handle Http operation that failed.
   * Let the app continue.
   * @param operation - name of the operation that failed
   * @param result - optional value to return as the observable result
   */
  private handleError<T> (operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {

      console.error(error);
      console.error('Failed on ' + operation);

      // Let the app keep running by returning an empty result.
      return of(result as T);
    };
  }

}
