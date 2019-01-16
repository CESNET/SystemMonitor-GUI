import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Observable, of } from 'rxjs';
import { catchError, map, tap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root',
})
export class ImageService {

  constructor(
    private http: HttpClient
  ) {
  }

  /**
   * Returns an image from server, based on image name
   * @param imageUrl - Path to requested image relative to Munin home folder
   * @note '../' in imageUrl is not supported.
   */
  getImage(imageUrl: string): Observable<Blob> {
    return this.http.get('/monitor/graph/' + imageUrl, { responseType: 'blob' });
  }

}

