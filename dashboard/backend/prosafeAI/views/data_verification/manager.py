import json
from typing import Any, Dict, List, Tuple

import yaml


class DataRequirementsManager:
    """
    Manager for safety artifact "AI data requirements catalog" with the following capabilities:

    - Read "AI data requirements catalog"
    - Validate "AI data requirements catalog" against schema
    """

    # error message templates
    MISSING_KEY = "Missing key - '{}' (element id='{}')"
    UNEXPECTED_KEY = "Unexpected key - '{}' (element id='{})'"
    UNEXPECTED_TYPE = (
        "Unexpected data type - Actual: '{}' Expected: '{}' (key='{}', element id='{}')"
    )
    UNEXPECTED_VALUE = (
        "Unexpected value - Actual: '{}' Expected: {} (key='{}', element id='{}')"
    )
    DATA_AND_TEXTUAL_EXPORT = (
        "Wrong export type - Requirement must be machine_readable (element id='{}')"
    )

    @classmethod
    def read_requirements(
        cls, data_requirements_catalog_path: str
    ) -> Dict[str, Dict[str, Any]]:
        """
        Reads "AI data requirements catalog" from a given path. Automatically applies a sanity check and filters
        out requirements with ``type = "info"`` and ``export = "textual"``.

        Parameters
        ----------
        data_requirements_catalog_path
            Path to "AI data requirements catalog" (JSON file)

        Returns
        -------
        data_requirements
            The validated and filtered "AI data requirements catalog" (dict)
        """

        with open(data_requirements_catalog_path, "r") as content_file:
            content = json.load(content_file)

        validated_requirements_specification = cls._validate_requirements_schema(
            content
        )
        return cls._remove_textual_requirements(validated_requirements_specification)

    @classmethod
    def read_data_names_mapping(cls, data_names_mapping_path: str) -> Dict[str, Any]:
        with open(data_names_mapping_path, "r") as content_file:
            content = yaml.safe_load(content_file)

        validated_data_names_mapping = cls._validate_data_names_mapping_schema(content)
        return validated_data_names_mapping

    @staticmethod
    def _remove_textual_requirements(
        data_requirements_catalog: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Dict[str, Any]]:
        """
        Removes requirements of ``type = "info"`` and ``export = "textual"`` from a sanity checked
        "AI data requirements catalog"

        Parameters
        ----------
        data_requirements_catalog
            The unfiltered "AI data requirements catalog"

        Returns
        -------
        data_requirements
            The filtered "AI data requirements catalog"
        """

        filtered_requirements = []
        requirements = data_requirements_catalog["requirements_catalog"]["requirements"]

        for requirement in requirements:
            if requirement["export"] == "machine_readable":
                filtered_requirements.append(requirement)

        filtered_specification = data_requirements_catalog.copy()
        filtered_specification["requirements_catalog"][
            "requirements"
        ] = filtered_requirements
        return filtered_specification

    @classmethod
    def _validate_data_names_mapping_schema(
        cls, data_names_mapping: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Applies sanity check on given ``data_names_mapping`` in respect of the structure
        defined in the ``schema``

        Parameters
        ----------
        data_names_mapping
            The ``data_names_mapping`` that needs to be sanity checked

        Returns
        -------
            The sanity checked ``data_names_mapping``
        """

        # template schema configurations -> "expected_key": (expected_type, accepts_none, expected_values, is_required)
        root_schema = {
            "requirements_to_ignore": (list, True, None, False),
            "data_description": (dict, False, None, True),
            "check_classes": (dict, True, None, False),
        }
        data_description_values_schema = {
            "name_in_data": (str, True, None, True),
            "nesting_level": (int, True, None, False),
            "comes_from": (str, False, {"plugin", "input"}, False),
        }

        error_log = []

        _, findings = cls._check_section(
            root_schema, data_names_mapping, "data_names_mapping"
        )
        error_log += findings

        if "data_description" in data_names_mapping.keys():
            for data_descr_name, data_descr_values in data_names_mapping[
                "data_description"
            ].items():
                _, findings = cls._check_section(
                    data_description_values_schema, data_descr_values, data_descr_name
                )
                error_log += findings

                current_data_dscr = data_names_mapping["data_description"][
                    data_descr_name
                ]

                if "comes_from" not in current_data_dscr.keys():
                    current_data_dscr["comes_from"] = "plugin"

                if "nesting_level" not in current_data_dscr.keys():
                    current_data_dscr["nesting_level"] = None

        if (
            "requirements_to_ignore" not in data_names_mapping.keys()
            or data_names_mapping["requirements_to_ignore"] is None
        ):
            data_names_mapping["requirements_to_ignore"] = []

        if (
            "check_classes" not in data_names_mapping.keys()
            or data_names_mapping["check_classes"] is None
        ):
            data_names_mapping["check_classes"] = dict()

        if error_log:
            cls._raise_value_error(
                validated_file_name="Data names mapping", error_log=error_log
            )

        return data_names_mapping

    @classmethod
    def _validate_requirements_schema(
        cls, data_requirements_catalog: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Dict[str, Any]]:
        """
        Applies sanity check on given "AI data requirements catalog" in respect of the structure
        defined in the ``schema``

        Parameters
        ----------
        data_requirements_catalog
            The "AI data requirements catalog" that needs to be sanity checked

        Returns
        -------
        requirements_specification
            The sanity checked "AI data requirements catalog"

        Raises
        ------
        ValueError
            Will get raised when the schema validation fails, including all findings in the error message.
            The following issues will lead to a failure:

            - Missing or unexpected keys
            - Unexpected data types
            - Unexpected values
            - Requirements with ``type = "data"`` and ``export = "textual"``

        """

        # template schema configurations -> "expected_key": (expected_type, accepts_none, expected_values, is_required)
        root_schema = {"requirements_catalog": (dict, False, None, True)}
        catalog_schema = {
            "name": (str, False, None, True),
            "id": (str, False, None, True),
            "requirements": (list, False, None, True),
        }
        requirement_schema = {
            "name": (str, False, None, True),
            "id": (str, False, None, True),
            "type": (str, False, {"data", "info"}, True),
            "classification": (
                str,
                False,
                {"consistency", "accuracy", "representativeness"},
                True,
            ),
            "export": (str, False, {"machine_readable"}, True),
            "description": (dict, False, None, True),
        }
        description_schema = {
            "verification_object": (str, False, None, True),
            "verification_content": (str, False, None, True),
            "computation_rule": (dict, False, None, True),
        }

        error_log = []

        # check root
        _, findings = cls._check_section(
            root_schema, data_requirements_catalog, "Unknown"
        )
        error_log += findings

        # check catalog
        if "requirements_catalog" in data_requirements_catalog.keys():
            catalog_section = data_requirements_catalog["requirements_catalog"]
            _, findings = cls._check_section(catalog_schema, catalog_section)
            error_log += findings

            # check list of requirements
            if "requirements" in catalog_section.keys():
                requirements = catalog_section["requirements"]

                for requirement in requirements:
                    if not isinstance(requirement, dict):
                        error_log.append(
                            cls.UNEXPECTED_TYPE.format(
                                type(requirement).__name__,
                                dict.__name__,
                                "requirements",
                                "Unknown",
                            )
                        )
                        continue

                    if "export" in requirement.keys() and "type" in requirement.keys():
                        if (
                            requirement["type"] == "data"
                            and requirement["export"] == "textual"
                        ):
                            # requirements of type data and textual export lead to error
                            idx = (
                                requirement["id"]
                                if "id" in requirement.keys()
                                else "Unknown"
                            )
                            error_log.append(cls.DATA_AND_TEXTUAL_EXPORT.format(idx))
                            continue

                        elif (
                            requirement["type"] == "info"
                            and requirement["export"] == "textual"
                        ):
                            # requirements of type info and textual export get skipped
                            continue

                    idx, findings = cls._check_section(requirement_schema, requirement)
                    error_log += findings

                    if "description" in requirement.keys():
                        description = requirement["description"]
                        if isinstance(description, dict):
                            _, findings = cls._check_section(
                                description_schema, description, idx
                            )
                            error_log += findings

        if error_log:
            cls._raise_value_error(
                validated_file_name="Requirements catalog", error_log=error_log
            )

        return data_requirements_catalog

    @classmethod
    def _raise_value_error(cls, validated_file_name: str, error_log: List[str]):
        """
        Raises :class:`~.ValueError` with the given ``error_log`` in a formatted way

        Parameters
        ----------
        validated_file_name
            Name of the file that is being validated ("Data names mapping" or "Requirements catalog")

        error_log
            The error_log containing violations during the schema validation

        Returns
        -------
            None
        """
        error_log_nums = [f"{i + 1}.) {err}" for i, err in enumerate(error_log)]
        raise ValueError(
            f"Sanity check of '{validated_file_name}' failed due to {len(error_log)} issues:\n"
            + "\n".join(error_log_nums)
        )

    @classmethod
    def _check_section(
        cls,
        schema: Dict[str, Any],
        specification: Dict[str, Any],
        current_id: str = None,
    ) -> Tuple[str, List[str]]:
        """
        Validates the given section of the "AI data requirements catalog" in respect of the given ``schema``

        Parameters
        ----------
        schema
            Section of the "AI data requirements catalog" schema
        specification
            Section of the actual "AI data requirements catalog" that needs to be validated
        current_id
            The id of the current section, used to generate descriptive error message

        Returns
        -------
        current_id
            The id of the current section of the "AI data requirements catalog"
        findings
            List containing error messages when violations against the schema were found, otherwise it's empty
        """

        findings = []
        if not current_id:
            current_id = (
                specification["id"] if "id" in specification.keys() else "Unknown"
            )

        for spec_key in specification.keys():
            if spec_key not in schema.keys():
                findings.append(cls.UNEXPECTED_KEY.format(spec_key, current_id))

        for config_key in schema.keys():
            config_type, accepts_none, config_values, is_required = schema[config_key]

            if config_key in specification.keys():
                spec_value = specification[config_key]
                spec_type = type(spec_value)

                if not isinstance(spec_value, config_type):
                    if spec_value is not None or (
                        spec_value is None and not accepts_none
                    ):
                        findings.append(
                            cls.UNEXPECTED_TYPE.format(
                                spec_type.__name__,
                                config_type.__name__,
                                config_key,
                                current_id,
                            )
                        )

                if config_values and spec_value not in config_values:
                    findings.append(
                        cls.UNEXPECTED_VALUE.format(
                            spec_value, config_values, config_key, current_id
                        )
                    )
            elif is_required:
                findings.append(cls.MISSING_KEY.format(config_key, current_id))

        return current_id, findings
