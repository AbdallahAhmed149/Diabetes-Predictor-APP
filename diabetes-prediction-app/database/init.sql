-- Create Users table
create table if not exists users (
   id              serial primary key,
   email           varchar(255) unique not null,
   hashed_password varchar(255) not null,
   full_name       varchar(255) not null,
   role            varchar(20) not null check ( role in ( 'doctor',
                                                'patient' ) ),
   created_at      timestamp default current_timestamp,
   updated_at      timestamp default current_timestamp
);

-- Create Patients table
create table if not exists patients (
   id                serial primary key,
   user_id           integer
      references users ( id )
         on delete cascade,
   patient_code      varchar(50) unique,
   date_of_birth     date,
   phone             varchar(20),
   address           text,
   emergency_contact varchar(255),
   created_at        timestamp default current_timestamp,
   updated_at        timestamp default current_timestamp
);

-- Create Predictions table
create table if not exists predictions (
   id                                 serial primary key,
   patient_id                         integer
      references patients ( id )
         on delete cascade,
   doctor_id                          integer
      references users ( id ),
   
   -- Demographics (7 fields)
   age                                integer,
   gender                             varchar(20),
   ethnicity                          varchar(50),
   education_level                    varchar(50),
   income_level                       varchar(50),
   employment_status                  varchar(50),
   smoking_status                     varchar(50),
   
   -- Lifestyle (5 fields)
   alcohol_consumption_per_week       decimal,
   physical_activity_minutes_per_week integer,
   diet_score                         decimal,
   sleep_hours_per_day                decimal,
   screen_time_hours_per_day          decimal,
   
   -- Medical History (3 fields)
   family_history_diabetes            boolean,
   hypertension_history               boolean,
   cardiovascular_history             boolean,
   
   -- Physical Measurements (5 fields)
   bmi                                decimal,
   waist_to_hip_ratio                 decimal,
   systolic_bp                        integer,
   diastolic_bp                       integer,
   heart_rate                         integer,
   
   -- Lab Results (9 fields)
   cholesterol_total                  decimal,
   hdl_cholesterol                    decimal,
   ldl_cholesterol                    decimal,
   triglycerides                      decimal,
   glucose_fasting                    decimal,
   glucose_postprandial               decimal,
   insulin_level                      decimal,
   hba1c                              decimal,
   diabetes_risk_score                decimal,
   
   -- Prediction Results
   risk_probability                   decimal,
   risk_level                         varchar(20),
   prediction_class                   integer,
   created_at                         timestamp default current_timestamp
);

-- Create indexes for better performance
create index if not exists idx_users_email on
   users (
      email
   );
create index if not exists idx_patients_code on
   patients (
      patient_code
   );
create index if not exists idx_predictions_patient on
   predictions (
      patient_id
   );
create index if not exists idx_predictions_doctor on
   predictions (
      doctor_id
   );
create index if not exists idx_predictions_created on
   predictions (
      created_at
   );