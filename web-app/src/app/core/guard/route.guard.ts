import { Injectable }   from "@angular/core";
import { ActivatedRouteSnapshot, Router, RouterStateSnapshot } from "@angular/router";
import { Observable }   from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class RouteChildGuard {
    private permission: Array<any> = [];

    constructor(private router: Router) {
        
        
    }

    canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): Observable<boolean> | boolean {
        // let routePermission = route.data['permission'] || [];
        // let flag = false;
        // this.permission = JSON.parse(localStorage.getItem("permission")) || [];

        // for (let i = 0; i < this.permission.length; i++) {
        //     let inc =  routePermission.includes(this.permission[i]);

        //     if (inc) {
        //         flag = inc;
        //         break;
        //     }
        // }

        // if (this.permission.length == 0 || (routePermission.length > 0 && !flag) ) {
        //     this.router.navigate(['/deny']);
        //     return false;
        // }

        return true;
    }

    canActivateChild(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): Observable<boolean> | boolean {
        // this.permission = JSON.parse(localStorage.getItem("permission")) || [];
        
        // const routePermission = route.data.permission;
        // const boolPermission = this.permission.indexOf(routePermission);
        // if (this.permission.length == 0 || (routePermission && boolPermission === -1 )) {
        //     this.router.navigate(['/deny']);
        //     return false;
        // }
        let roleId = localStorage.getItem('roleIdLogin');
        if (0 === Number(roleId)) {
            this.router.navigate(['/deny']);
            return false;
        }

        return true;
    }
}
