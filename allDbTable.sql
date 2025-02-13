CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


CREATE TABLE public.experiences (
    user_id integer NOT NULL,
    prof_id integer NOT NULL,
    years integer NOT NULL,
    id integer NOT NULL
);

CREATE TABLE public.professions (
    title character varying(32) NOT NULL,
    id integer NOT NULL
);

CREATE TABLE public.projects (
    title character varying(32) NOT NULL,
    "desc" character varying(256) NOT NULL,
    owner_id integer NOT NULL,
    id integer NOT NULL
);


CREATE TABLE public.projects_workers (
    project_id integer NOT NULL,
    worker_id integer NOT NULL,
    id integer NOT NULL
);

CREATE TABLE public.users (
    first_name character varying(32) NOT NULL,
    second_name character varying(32) NOT NULL,
    phone character varying(32) NOT NULL,
    email character varying(32) NOT NULL,
    birthday date NOT NULL,
    role_id integer NOT NULL,
    time_created timestamp without time zone DEFAULT now() NOT NULL,
    id integer NOT NULL
);


CREATE TABLE public.users_roles (
    title character varying(32) NOT NULL,
    id integer NOT NULL
);

ALTER TABLE ONLY public.experiences ALTER COLUMN id SET DEFAULT nextval('public.experiences_id_seq'::regclass);

ALTER TABLE ONLY public.professions ALTER COLUMN id SET DEFAULT nextval('public.professions_id_seq'::regclass);


ALTER TABLE ONLY public.projects ALTER COLUMN id SET DEFAULT nextval('public.projects_id_seq'::regclass);


ALTER TABLE ONLY public.projects_workers ALTER COLUMN id SET DEFAULT nextval('public.projects_workers_id_seq'::regclass);

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);

ALTER TABLE ONLY public.users_roles ALTER COLUMN id SET DEFAULT nextval('public.users_roles_id_seq'::regclass);


ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);

ALTER TABLE ONLY public.experiences
    ADD CONSTRAINT pk_experiences PRIMARY KEY (id);

ALTER TABLE ONLY public.professions
    ADD CONSTRAINT pk_professions PRIMARY KEY (id);

ALTER TABLE ONLY public.projects
    ADD CONSTRAINT pk_projects PRIMARY KEY (id);

ALTER TABLE ONLY public.projects_workers
    ADD CONSTRAINT pk_projects_workers PRIMARY KEY (id);

ALTER TABLE ONLY public.users
    ADD CONSTRAINT pk_users PRIMARY KEY (id);

ALTER TABLE ONLY public.users_roles
    ADD CONSTRAINT pk_users_roles PRIMARY KEY (id);


ALTER TABLE ONLY public.experiences
    ADD CONSTRAINT fk_experiences_prof_id_professions FOREIGN KEY (prof_id) REFERENCES public.professions(id);

ALTER TABLE ONLY public.experiences
    ADD CONSTRAINT fk_experiences_user_id_users FOREIGN KEY (user_id) REFERENCES public.users(id);


ALTER TABLE ONLY public.projects
    ADD CONSTRAINT fk_projects_owner_id_users FOREIGN KEY (owner_id) REFERENCES public.users(id);

ALTER TABLE ONLY public.projects_workers
    ADD CONSTRAINT fk_projects_workers_project_id_projects FOREIGN KEY (project_id) REFERENCES public.projects(id);

ALTER TABLE ONLY public.projects_workers
    ADD CONSTRAINT fk_projects_workers_worker_id_users FOREIGN KEY (worker_id) REFERENCES public.users(id);

ALTER TABLE ONLY public.users
    ADD CONSTRAINT fk_users_role_id_users_roles FOREIGN KEY (role_id) REFERENCES public.users_roles(id);
