function [ success, qs, qnear ] = FR_New_Config( qs, qnear, J, Jt )
    success = TRUE;
    qr = qs;
    dx_err = Compute_Task_Error(qs, qnear);
    while sqrt(sumsqr(dx_err)) > eps(1)
        qs = Retract_Config(qs, dx_error, Jt);
        if sqrt(sumsqr(qs - qr)) > sqrt(sumsqr(qr - qnear))
            success = FALSE;
            break
        end
        dx_err = Compute_Task_Error(qs, qnear)
    end
    if InCollision(qs)
        success = FALSE
    end
end

function [ qs ] = Retract_Config(q, dx, Jt)
    dq = Jt * dx;
    qs = q - dq
end