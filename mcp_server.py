"""DORA MCP Server - DevOps Research and Assessment metrics MCP server."""

from datetime import datetime
from typing import Any

from mcp.server.fastmcp import FastMCP

# Create the DORA MCP server
mcp = FastMCP("DORA Metrics Server")


@mcp.tool()
def get_deployment_frequency(
    deployments: int, days: int = 30
) -> dict[str, Any]:
    """Calculate deployment frequency metric.

    Args:
        deployments: Number of deployments in the period
        days: Number of days in the measurement period (default: 30)

    Returns:
        Dictionary containing deployment frequency metrics and performance level
    """
    if days <= 0:
        return {"error": "Days must be positive"}
    if deployments < 0:
        return {"error": "Deployments cannot be negative"}

    frequency = deployments / days

    # Determine performance level based on DORA benchmarks
    if frequency >= 1:
        level = "Elite"
        description = "Multiple deploys per day"
    elif frequency >= 1 / 7:
        level = "High"
        description = "Between once per day and once per week"
    elif frequency >= 1 / 30:
        level = "Medium"
        description = "Between once per week and once per month"
    else:
        level = "Low"
        description = "Less than once per month"

    return {
        "metric": "deployment_frequency",
        "deployments": deployments,
        "days": days,
        "frequency_per_day": round(frequency, 4),
        "performance_level": level,
        "description": description,
        "calculated_at": datetime.now().isoformat(),
    }


@mcp.tool()
def get_lead_time_for_changes(
    commit_to_deploy_hours: list[float],
) -> dict[str, Any]:
    """Calculate lead time for changes metric.

    Args:
        commit_to_deploy_hours: List of hours from commit to deployment for each change

    Returns:
        Dictionary containing lead time metrics and performance level
    """
    if not commit_to_deploy_hours:
        return {"error": "No data provided"}
    if any(h < 0 for h in commit_to_deploy_hours):
        return {"error": "Hours cannot be negative"}

    avg_hours = sum(commit_to_deploy_hours) / len(commit_to_deploy_hours)
    avg_days = avg_hours / 24

    # Determine performance level based on DORA benchmarks
    if avg_days < 1:
        level = "Elite"
        description = "Less than one day"
    elif avg_days <= 7:
        level = "High"
        description = "Between one day and one week"
    elif avg_days <= 30:
        level = "Medium"
        description = "Between one week and one month"
    else:
        level = "Low"
        description = "More than one month"

    return {
        "metric": "lead_time_for_changes",
        "sample_size": len(commit_to_deploy_hours),
        "average_hours": round(avg_hours, 2),
        "average_days": round(avg_days, 2),
        "min_hours": round(min(commit_to_deploy_hours), 2),
        "max_hours": round(max(commit_to_deploy_hours), 2),
        "performance_level": level,
        "description": description,
        "calculated_at": datetime.now().isoformat(),
    }


@mcp.tool()
def get_change_failure_rate(
    total_deployments: int, failed_deployments: int
) -> dict[str, Any]:
    """Calculate change failure rate metric.

    Args:
        total_deployments: Total number of deployments
        failed_deployments: Number of deployments that caused failures

    Returns:
        Dictionary containing change failure rate metrics and performance level
    """
    if total_deployments <= 0:
        return {"error": "Total deployments must be positive"}
    if failed_deployments < 0:
        return {"error": "Failed deployments cannot be negative"}
    if failed_deployments > total_deployments:
        return {"error": "Failed deployments cannot exceed total deployments"}

    failure_rate = (failed_deployments / total_deployments) * 100

    # Determine performance level based on DORA benchmarks
    if failure_rate <= 15:
        level = "Elite/High"
        description = "0-15% failure rate"
    elif failure_rate <= 30:
        level = "Medium"
        description = "16-30% failure rate"
    else:
        level = "Low"
        description = "More than 30% failure rate"

    return {
        "metric": "change_failure_rate",
        "total_deployments": total_deployments,
        "failed_deployments": failed_deployments,
        "failure_rate_percent": round(failure_rate, 2),
        "performance_level": level,
        "description": description,
        "calculated_at": datetime.now().isoformat(),
    }


@mcp.tool()
def get_mean_time_to_recovery(
    recovery_times_hours: list[float],
) -> dict[str, Any]:
    """Calculate Mean Time to Recovery (MTTR) metric.

    Args:
        recovery_times_hours: List of recovery times in hours for each incident

    Returns:
        Dictionary containing MTTR metrics and performance level
    """
    if not recovery_times_hours:
        return {"error": "No data provided"}
    if any(h < 0 for h in recovery_times_hours):
        return {"error": "Recovery times cannot be negative"}

    avg_hours = sum(recovery_times_hours) / len(recovery_times_hours)

    # Determine performance level based on DORA benchmarks
    if avg_hours < 1:
        level = "Elite"
        description = "Less than one hour"
    elif avg_hours <= 24:
        level = "High"
        description = "Less than one day"
    elif avg_hours <= 168:  # 7 days
        level = "Medium"
        description = "Less than one week"
    else:
        level = "Low"
        description = "More than one week"

    return {
        "metric": "mean_time_to_recovery",
        "sample_size": len(recovery_times_hours),
        "average_hours": round(avg_hours, 2),
        "min_hours": round(min(recovery_times_hours), 2),
        "max_hours": round(max(recovery_times_hours), 2),
        "performance_level": level,
        "description": description,
        "calculated_at": datetime.now().isoformat(),
    }


@mcp.tool()
def get_dora_summary(
    deployment_frequency_per_day: float,
    lead_time_days: float,
    change_failure_rate_percent: float,
    mttr_hours: float,
) -> dict[str, Any]:
    """Get a summary of all four DORA metrics with overall performance assessment.

    Args:
        deployment_frequency_per_day: Average deployments per day
        lead_time_days: Average lead time in days
        change_failure_rate_percent: Failure rate as percentage (0-100)
        mttr_hours: Mean time to recovery in hours

    Returns:
        Dictionary containing summary of all DORA metrics and overall performance
    """
    metrics = {}

    # Deployment Frequency
    if deployment_frequency_per_day >= 1:
        metrics["deployment_frequency"] = {"level": "Elite", "score": 4}
    elif deployment_frequency_per_day >= 1 / 7:
        metrics["deployment_frequency"] = {"level": "High", "score": 3}
    elif deployment_frequency_per_day >= 1 / 30:
        metrics["deployment_frequency"] = {"level": "Medium", "score": 2}
    else:
        metrics["deployment_frequency"] = {"level": "Low", "score": 1}

    # Lead Time for Changes
    if lead_time_days < 1:
        metrics["lead_time_for_changes"] = {"level": "Elite", "score": 4}
    elif lead_time_days <= 7:
        metrics["lead_time_for_changes"] = {"level": "High", "score": 3}
    elif lead_time_days <= 30:
        metrics["lead_time_for_changes"] = {"level": "Medium", "score": 2}
    else:
        metrics["lead_time_for_changes"] = {"level": "Low", "score": 1}

    # Change Failure Rate (DORA combines Elite/High as 0-15%)
    if change_failure_rate_percent <= 15:
        metrics["change_failure_rate"] = {"level": "Elite/High", "score": 4}
    elif change_failure_rate_percent <= 30:
        metrics["change_failure_rate"] = {"level": "Medium", "score": 3}
    else:
        metrics["change_failure_rate"] = {"level": "Low", "score": 1}

    # MTTR
    if mttr_hours < 1:
        metrics["mean_time_to_recovery"] = {"level": "Elite", "score": 4}
    elif mttr_hours <= 24:
        metrics["mean_time_to_recovery"] = {"level": "High", "score": 3}
    elif mttr_hours <= 168:
        metrics["mean_time_to_recovery"] = {"level": "Medium", "score": 2}
    else:
        metrics["mean_time_to_recovery"] = {"level": "Low", "score": 1}

    # Calculate overall score
    total_score = sum(m["score"] for m in metrics.values())
    avg_score = total_score / 4

    if avg_score >= 3.5:
        overall_level = "Elite"
    elif avg_score >= 2.5:
        overall_level = "High"
    elif avg_score >= 1.5:
        overall_level = "Medium"
    else:
        overall_level = "Low"

    return {
        "metrics": metrics,
        "total_score": total_score,
        "average_score": round(avg_score, 2),
        "overall_performance": overall_level,
        "calculated_at": datetime.now().isoformat(),
    }


def main() -> None:
    """Run the DORA MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
