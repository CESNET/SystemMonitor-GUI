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
  getPatterns(): Observable<Pattern[]> {
    return this.http.get<Pattern[]>('/monitor/patterns').pipe(
      catchError(this.handleError('getPatterns', []))
    );
  }

  /**
   * GET links to graphs by category from backend
   * To get list of graphs for dashboard, set category to "default"
   * @param category - Category name to get graphs from.
   */
  getGraphs(category: string): Observable<string[]> {
    return this.http.get<string[]>('/monitor/graphs/' + category).pipe(
      catchError(this.handleError('getGraphs', []))
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
      console.error('Failed on ' + operation);
      console.error(error);
      //TODO: Notify user in GUI
      // Let the app keep running by returning an empty result.
      return of(result as T);
    };
  }

}
