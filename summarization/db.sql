--
-- PostgreSQL database dump
--

-- Dumped from database version 12.18 (Ubuntu 12.18-0ubuntu0.20.04.1)
-- Dumped by pg_dump version 12.18 (Ubuntu 12.18-0ubuntu0.20.04.1)

--
-- Name: summarydb; Type: DATABASE; Schema: -; Owner: 
--

-- Create a user for postgresql called 'ctillm':

-- ```bash
-- createuser ctillm
-- ```
-- Note: you might have to do this as 'postgres' user from the shell



CREATE DATABASE summarydb WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'en_US.UTF-8' LC_CTYPE = 'en_US.UTF-8';


ALTER DATABASE summarydb OWNER TO ctillm;

\connect summarydb

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

GRANT ALL on DATABASE SUMMARYDB to ctillm;

--
-- Name: summary; Type: TABLE; Schema: public; Owner: ctillm
--

CREATE TABLE public.summary (
    id integer NOT NULL,
    url text,
    summary text,
    date date,
    score double precision,
    human_summary text,
    evaluator_reasoning text,
	original_text text,
	sha256_original_text varchar(64),
    llm_response jsonb,
    llm character varying(255)
);


ALTER TABLE public.summary OWNER TO ctillm;

--
-- Name: summary_id_seq; Type: SEQUENCE; Schema: public; Owner: ctillm
--

CREATE SEQUENCE public.summary_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.summary_id_seq OWNER TO ctillm;

--
-- Name: summary_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ctillm
--

ALTER SEQUENCE public.summary_id_seq OWNED BY public.summary.id;


--
-- Name: summary id; Type: DEFAULT; Schema: public; Owner: ctillm
--

ALTER TABLE ONLY public.summary ALTER COLUMN id SET DEFAULT nextval('public.summary_id_seq'::regclass);


--
-- Name: summary summary_pkey; Type: CONSTRAINT; Schema: public; Owner: ctillm
--

ALTER TABLE ONLY public.summary
    ADD CONSTRAINT summary_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

